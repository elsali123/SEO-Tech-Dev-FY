import pygame
import random

class DragNestMinigame:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 36)
        self.small_font = pygame.font.SysFont('Arial', 28)
        self.button_rect = pygame.Rect(0, 0, 180, 60)
        self.button_rect.center = (screen.get_width() // 2, screen.get_height() - 80)
        self.running = True
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.nest_rect = pygame.Rect(self.width // 2 - 80, self.height // 2 + 100, 160, 80)
        self.reset_game()

    def reset_game(self):
        # Place 3 chicks at random positions
        self.chicks = []
        for _ in range(3):
            x = random.randint(100, self.width - 100)
            y = random.randint(100, self.height // 2)
            self.chicks.append({'pos': [x, y], 'dragging': False, 'offset': (0, 0)})
        self.chick_radius = 32
        self.selected = None
        self.game_over = False

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.game_over and self.button_rect.collidepoint(event.pos):
                        self.running = False
                    elif not self.game_over:
                        for i, chick in enumerate(self.chicks):
                            cx, cy = chick['pos']
                            if (event.pos[0] - cx) ** 2 + (event.pos[1] - cy) ** 2 < self.chick_radius ** 2:
                                chick['dragging'] = True
                                chick['offset'] = (cx - event.pos[0], cy - event.pos[1])
                                self.selected = i
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.selected is not None:
                        self.chicks[self.selected]['dragging'] = False
                        self.selected = None
                        if self.all_in_nest():
                            self.game_over = True
                if event.type == pygame.MOUSEMOTION:
                    if self.selected is not None and self.chicks[self.selected]['dragging']:
                        self.chicks[self.selected]['pos'][0] = event.pos[0] + self.chicks[self.selected]['offset'][0]
                        self.chicks[self.selected]['pos'][1] = event.pos[1] + self.chicks[self.selected]['offset'][1]
            self.draw_game()
            pygame.display.flip()
            clock.tick(60)

    def all_in_nest(self):
        for chick in self.chicks:
            cx, cy = chick['pos']
            if not self.nest_rect.collidepoint(cx, cy):
                return False
        return True

    def draw_game(self):
        self.screen.fill((30, 30, 30))
        # Draw nest
        pygame.draw.ellipse(self.screen, (180, 120, 40), self.nest_rect)
        nest_text = self.small_font.render('Nest', True, (80, 40, 0))
        nest_rect = nest_text.get_rect(center=self.nest_rect.center)
        self.screen.blit(nest_text, nest_rect)
        # Draw chicks
        colors = [(255, 200, 0), (255, 100, 0), (255, 255, 100)]
        for i, chick in enumerate(self.chicks):
            pygame.draw.circle(self.screen, colors[i % len(colors)], chick['pos'], self.chick_radius)
            eye_x = chick['pos'][0] + 10
            eye_y = chick['pos'][1] - 10
            pygame.draw.circle(self.screen, (0, 0, 0), (eye_x, eye_y), 5)
        # Draw win message
        if self.game_over:
            msg = 'All chicks safe!'
            color = (0, 255, 100)
            msg_surf = self.font.render(msg, True, color)
            msg_rect = msg_surf.get_rect(center=(self.width // 2, 60))
            self.screen.blit(msg_surf, msg_rect)
            pygame.draw.rect(self.screen, (70, 130, 180), self.button_rect, border_radius=10)
            btn_text = self.font.render('Back', True, (255, 255, 255))
            btn_rect = btn_text.get_rect(center=self.button_rect.center)
            self.screen.blit(btn_text, btn_rect) 