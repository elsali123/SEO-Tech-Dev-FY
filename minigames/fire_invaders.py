import pygame
import random

class FireInvadersMinigame:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 36)
        self.small_font = pygame.font.SysFont('Arial', 28)
        self.button_rect = pygame.Rect(0, 0, 180, 60)
        self.button_rect.center = (screen.get_width() // 2, screen.get_height() - 80)
        self.running = True
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Load assets
        try:
            self.background = pygame.image.load('assets/Minigame_assets/leaves.webp')
            self.background = pygame.transform.scale(self.background, (self.width, self.height))
        except pygame.error:
            print("Could not load background image, using default color")
            self.background = None
            
        try:
            self.fire_sprite = pygame.image.load('assets/Minigame_assets/fire.png')
            self.fire_sprite = pygame.transform.scale(self.fire_sprite, (44, 44))  # Scale to match original fire size
        except pygame.error:
            print("Could not load fire sprite, using default circles")
            self.fire_sprite = None
            
        self.reset_game()

    def reset_game(self):
        self.player_x = self.width // 2
        self.player_y = self.height - 60
        self.player_speed = 8
        self.bullets = []  # Each bullet is [x, y]
        self.bullet_speed = 12
        self.fires = []  # Each fire is [x, y]
        self.fire_speed = 3
        self.lives = 3
        self.score = 0
        self.max_fires = 2
        self.fire_spawn_timer = 0
        self.fire_spawn_delay = 100  # Frames between fire spawns (increased from implicit spawning)
        self.spawn_fires()
        self.game_over = False
        self.win = False

    def spawn_fires(self):
        self.fires = []
        for _ in range(self.max_fires):
            x = random.randint(40, self.width - 40)
            y = random.randint(-400, -40)
            self.fires.append([x, y])

    def spawn_new_fire(self):
        """Spawn a single new fire at random intervals"""
        if len(self.fires) < self.max_fires and not self.game_over:
            x = random.randint(40, self.width - 40)
            y = random.randint(-200, -40)
            self.fires.append([x, y])

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.game_over and self.button_rect.collidepoint(event.pos):
                        self.running = False
                if event.type == pygame.KEYDOWN and not self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.bullets.append([self.player_x, self.player_y - 30])
            keys = pygame.key.get_pressed()
            if not self.game_over:
                if keys[pygame.K_LEFT]:
                    self.player_x -= self.player_speed
                if keys[pygame.K_RIGHT]:
                    self.player_x += self.player_speed
                self.player_x = max(40, min(self.width - 40, self.player_x))

            self.update_game()
            self.draw_game()
            pygame.display.flip()
            clock.tick(60)

    def update_game(self):
        if self.game_over:
            return
            
        # Handle fire spawning timer
        self.fire_spawn_timer += 1
        if self.fire_spawn_timer >= self.fire_spawn_delay:
            self.spawn_new_fire()
            self.fire_spawn_timer = 0
            # Gradually decrease spawn delay to increase difficulty
            if self.fire_spawn_delay > 20:
                self.fire_spawn_delay -= 0.5
                
        # Move bullets
        for bullet in self.bullets:
            bullet[1] -= self.bullet_speed
        self.bullets = [b for b in self.bullets if b[1] > -20]
        
        # Move fires
        for fire in self.fires:
            fire[1] += self.fire_speed
            
        # Check collisions
        for bullet in self.bullets:
            for fire in self.fires:
                if abs(bullet[0] - fire[0]) < 30 and abs(bullet[1] - fire[1]) < 30:
                    if fire in self.fires:
                        self.fires.remove(fire)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    self.score += 1
                    break
                    
        # Check if fire reached bottom
        fires_to_remove = []
        for fire in self.fires:
            if fire[1] > self.height - 40:
                self.lives -= 1
                fires_to_remove.append(fire)
        for fire in fires_to_remove:
            self.fires.remove(fire)
            
        # Win/lose conditions
        if self.lives <= 0:
            self.game_over = True
            self.win = False
        elif self.score >= 5:  # Win condition based on score
            self.game_over = True
            self.win = True

    def draw_game(self):
        # Draw background
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((30, 30, 30))
            
        # Draw player (water cannon)
        pygame.draw.rect(self.screen, (70, 130, 255), (self.player_x - 25, self.player_y, 50, 30), border_radius=8)
        pygame.draw.rect(self.screen, (100, 180, 255), (self.player_x - 10, self.player_y - 20, 20, 20), border_radius=6)
        
        # Draw bullets
        for bullet in self.bullets:
            pygame.draw.rect(self.screen, (0, 200, 255), (bullet[0] - 5, bullet[1], 10, 20), border_radius=4)
            
        # Draw fires
        for fire in self.fires:
            if self.fire_sprite:
                # Center the sprite on the fire position
                sprite_rect = self.fire_sprite.get_rect(center=(fire[0], fire[1]))
                self.screen.blit(self.fire_sprite, sprite_rect)
            else:
                # Fallback to original circles if sprite fails to load
                pygame.draw.circle(self.screen, (255, 80, 0), (fire[0], fire[1]), 22)
                pygame.draw.circle(self.screen, (255, 200, 0), (fire[0], fire[1]), 12)
                
        # Draw HUD
        # Win condition text at top center
        win_text = self.small_font.render('To win, score over 5 points!', True, (255, 255, 255))
        win_text_rect = win_text.get_rect(center=(self.width // 2, 25))
        self.screen.blit(win_text, win_text_rect)
        
        lives_surf = self.small_font.render(f'Lives: {self.lives}', True, (255, 255, 255))
        score_surf = self.small_font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(lives_surf, (30, 50))  # Moved down slightly to avoid overlap
        self.screen.blit(score_surf, (self.screen.get_width() - 160, 50))  # Moved down slightly
        
        # Game over/win
        if self.game_over:
            msg = 'You Win!' if self.win else 'Game Over'
            color = (0, 255, 100) if self.win else (255, 80, 0)
            msg_surf = self.font.render(msg, True, color)
            msg_rect = msg_surf.get_rect(center=(self.width // 2, self.height // 2 - 40))
            self.screen.blit(msg_surf, msg_rect)
            pygame.draw.rect(self.screen, (70, 130, 180), self.button_rect, border_radius=10)
            btn_text = self.font.render('Back', True, (255, 255, 255))
            btn_rect = btn_text.get_rect(center=self.button_rect.center)
            self.screen.blit(btn_text, btn_rect)