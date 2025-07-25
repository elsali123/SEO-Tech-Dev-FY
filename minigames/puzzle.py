import pygame
import os
import random

class PuzzleMinigame:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 36)
        self.small_font = pygame.font.SysFont('Arial', 28)
        self.button_rect = pygame.Rect(0, 0, 180, 60)
        self.button_rect.center = (screen.get_width() // 2, screen.get_height() - 80)
        self.running = True
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.grid_size = 3
        self.tile_size = 160
        self.margin = 10
        self.puzzle_top = 100
        self.puzzle_left = (self.width - (self.grid_size * self.tile_size + (self.grid_size - 1) * self.margin)) // 2
        self.reset_game()

    def reset_game(self):
        # Load and slice rainforest image
        img_path = os.path.join('assets', 'background', 'rainforest.png')
        full_img = pygame.image.load(img_path).convert()
        full_img = pygame.transform.smoothscale(full_img, (self.grid_size * self.tile_size, self.grid_size * self.tile_size))
        self.tiles = []
        for y in range(self.grid_size):
            row = []
            for x in range(self.grid_size):
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                surf = pygame.Surface((self.tile_size, self.tile_size))
                surf.blit(full_img, (0, 0), rect)
                row.append(surf)
            self.tiles.append(row)
        # Create board state (numbers 0-8, 0 is empty)
        self.board = [i for i in range(self.grid_size * self.grid_size)]
        while True:
            random.shuffle(self.board)
            if self.is_solvable(self.board) and not self.is_solved():
                break
        self.game_over = False

    def is_solved(self):
        return self.board == list(range(self.grid_size * self.grid_size))

    def is_solvable(self, board):
        inv = 0
        for i in range(len(board)):
            for j in range(i + 1, len(board)):
                if board[i] and board[j] and board[i] > board[j]:
                    inv += 1
        return inv % 2 == 0

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
                        self.handle_click(event.pos)
            self.draw_game()
            pygame.display.flip()
            clock.tick(60)

    def handle_click(self, pos):
        x, y = pos
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                idx = row * self.grid_size + col
                tile_x = self.puzzle_left + col * (self.tile_size + self.margin)
                tile_y = self.puzzle_top + row * (self.tile_size + self.margin)
                rect = pygame.Rect(tile_x, tile_y, self.tile_size, self.tile_size)
                if rect.collidepoint(x, y):
                    self.try_move(idx)
                    return

    def try_move(self, idx):
        empty_idx = self.board.index(0)
        if self.is_adjacent(idx, empty_idx):
            self.board[empty_idx], self.board[idx] = self.board[idx], self.board[empty_idx]
            if self.is_solved():
                self.game_over = True

    def is_adjacent(self, idx1, idx2):
        row1, col1 = divmod(idx1, self.grid_size)
        row2, col2 = divmod(idx2, self.grid_size)
        return (abs(row1 - row2) == 1 and col1 == col2) or (abs(col1 - col2) == 1 and row1 == row2)

    def draw_game(self):
        self.screen.fill((30, 30, 30))
        # Draw puzzle tiles
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                idx = row * self.grid_size + col
                val = self.board[idx]
                tile_x = self.puzzle_left + col * (self.tile_size + self.margin)
                tile_y = self.puzzle_top + row * (self.tile_size + self.margin)
                if val != 0:
                    tile_img = self.tiles[val // self.grid_size][val % self.grid_size]
                    self.screen.blit(tile_img, (tile_x, tile_y))
        # Draw grid lines
        for row in range(self.grid_size + 1):
            y = self.puzzle_top + row * (self.tile_size + self.margin) - self.margin // 2
            pygame.draw.line(self.screen, (80, 80, 80), (self.puzzle_left, y), (self.puzzle_left + self.grid_size * (self.tile_size + self.margin) - self.margin, y), 2)
        for col in range(self.grid_size + 1):
            x = self.puzzle_left + col * (self.tile_size + self.margin) - self.margin // 2
            pygame.draw.line(self.screen, (80, 80, 80), (x, self.puzzle_top), (x, self.puzzle_top + self.grid_size * (self.tile_size + self.margin) - self.margin), 2)
        # Draw win message
        if self.game_over:
            msg = 'You Win!'
            color = (0, 255, 100)
            msg_surf = self.font.render(msg, True, color)
            msg_rect = msg_surf.get_rect(center=(self.width // 2, 60))
            self.screen.blit(msg_surf, msg_rect)
            pygame.draw.rect(self.screen, (70, 130, 180), self.button_rect, border_radius=10)
            btn_text = self.font.render('Back', True, (255, 255, 255))
            btn_rect = btn_text.get_rect(center=self.button_rect.center)
            self.screen.blit(btn_text, btn_rect) 