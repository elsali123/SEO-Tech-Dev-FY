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
        self.max_fires = 7
        self.spawn_fires()
        self.game_over = False
        self.win = False

    def spawn_fires(self):
        self.fires = []
        for _ in range(self.max_fires):
            x = random.randint(40, self.width - 40)
            y = random.randint(-400, -40)
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
        for fire in self.fires:
            if fire[1] > self.height - 40:
                self.lives -= 1
                self.fires.remove(fire)
        # Win/lose conditions
        if self.lives <= 0:
            self.game_over = True
            self.win = False
        elif not self.fires:
            self.game_over = True
            self.win = True

    def draw_game(self):
        self.screen.fill((30, 30, 30))
        # Draw player (water cannon)
        pygame.draw.rect(self.screen, (70, 130, 255), (self.player_x - 25, self.player_y, 50, 30), border_radius=8)
        pygame.draw.rect(self.screen, (100, 180, 255), (self.player_x - 10, self.player_y - 20, 20, 20), border_radius=6)
        # Draw bullets
        for bullet in self.bullets:
            pygame.draw.rect(self.screen, (0, 200, 255), (bullet[0] - 5, bullet[1], 10, 20), border_radius=4)
        # Draw fires
        for fire in self.fires:
            pygame.draw.circle(self.screen, (255, 80, 0), (fire[0], fire[1]), 22)
            pygame.draw.circle(self.screen, (255, 200, 0), (fire[0], fire[1]), 12)
        # Draw HUD
        lives_surf = self.small_font.render(f'Lives: {self.lives}', True, (255, 255, 255))
        score_surf = self.small_font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(lives_surf, (30, 20))
        self.screen.blit(score_surf, (self.screen.get_width() - 160, 20))
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