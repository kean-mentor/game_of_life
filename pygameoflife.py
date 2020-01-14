import random
import sys

import pygame


BOARD_SIZE = WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
BG_COLOR = 0, 0, 0
ALIVE_COLOR = 0, 255, 255
# DEAD_COLOR = 127, 127, 127
MAX_FPS = 5


class LifeGame:
    def __init__(self):
        pygame.init()
        self.is_paused = False
        self.screen = pygame.display.set_mode(BOARD_SIZE)

        self.clear_screen()
        pygame.display.flip()
        
        self.init_grids()

    def init_grids(self):
        self.num_cols = int(WIDTH / CELL_SIZE)
        self.num_rows = int(HEIGHT / CELL_SIZE)
        self.grids = ([[0 for _ in range(self.num_cols)] for _ in range(self.num_rows)],
                      [[0 for _ in range(self.num_cols)] for _ in range(self.num_rows)])    
        self.active_grid = 0

        self.randomize_gird()
        self.draw_grid()

    def randomize_gird(self):
        # self.grids[self.active_grid][25][25] = 1
        # self.grids[self.active_grid][25][26] = 1
        # self.grids[self.active_grid][6][5] = 1
        # self.grids[self.active_grid][26][26] = 1
        # self.grids[self.active_grid][24][31] = 1
        # self.grids[self.active_grid][26][30] = 1
        # self.grids[self.active_grid][26][31] = 1
        # self.grids[self.active_grid][26][32] = 1
        # return

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self.grids[self.active_grid][row][col] = random.choice([0, 1])

    def clear_screen(self):
        self.screen.fill(BG_COLOR)

    def get_next_status(self, row, col):
        neighbours = 0
        for r in range(max(0, row - 1), min(self.num_rows, row + 2)):
            for c in range(max(0, col - 1), min(self.num_cols, col + 2)):
                if self.grids[self.active_grid][r][c]:
                    neighbours += 1
        neighbours -= self.grids[self.active_grid][row][col]

        if neighbours in (2, 3):
            if not self.grids[self.active_grid][row][col] and neighbours == 3:
                return 1
            else:
                return self.grids[self.active_grid][row][col]
        if neighbours < 2 or neighbours > 3:
            return 0

    def update_generation(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self.grids[(self.active_grid + 1) % 2][row][col] = self.get_next_status(row, col)

        if self.active_grid == 0:
            self.active_grid = 1
        else:
            self.active_grid = 0

    def draw_grid(self):
        self.clear_screen()

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.grids[self.active_grid][row][col]:
                    pygame.draw.circle(
                        self.screen,
                        ALIVE_COLOR,
                        (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                        CELL_SIZE // 2, 0)

        pygame.display.flip()

    def run(self):
        last_update_completed = pygame.time.get_ticks()
        milliseconds_between_updates = int(1.0 / MAX_FPS * 1000)

        while True:
            self.handle_events()
            if not self.is_paused:
                self.update_generation()
                self.draw_grid()

            now = pygame.time.get_ticks()
            if now - last_update_completed < milliseconds_between_updates:
                pygame.time.delay(milliseconds_between_updates - (now - last_update_completed))
            last_update_completed = pygame.time.get_ticks()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.randomize_gird()
                    self.draw_grid()
                elif event.key == pygame.K_p:
                    self.is_paused = not self.is_paused
                elif event.key == pygame.K_SPACE and self.is_paused:
                    self.update_generation()
                    self.draw_grid()


if __name__ == "__main__":
    game = LifeGame()
    game.run()
