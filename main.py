import pygame
import numpy as np
from pygame_widgets.button import Button
from pygame.locals import *
import sys


def create_minefield(dim, num_mines):
    field = np.zeros((dim, dim), dtype=int)
    indices = np.random.choice(dim * dim, num_mines, replace=False)
    for index in indices:
        row = index // dim
        col = index % dim
        field[row, col] = -1
    return field


def create_adjacent_count_minefield(field: np.ndarray):
    field_copied = field.copy()
    for r in range(len(field_copied)):
        for c in range(len(field_copied[r])):
            if field_copied[r, c] != -1:
                field_copied[r, c] = count_adjacent_mines(field, r, c)
    return field_copied


def count_adjacent_mines(field, row, col):
    count = 0
    for r in range(max(0, row-1), min(DIM, row+2)):
        for c in range(max(0, col-1), min(DIM, col+2)):
            if field[r, c] == -1:
                count += 1
    return count


def reveal_cell(revealed, minefield, row, col):
    if not revealed[row, col]:
        revealed[row, col] = True
        if minefield[row, col] == 0:
            for r in range(max(0, row-1), min(DIM, row+2)):
                for c in range(max(0, col-1), min(DIM, col+2)):
                    reveal_cell(revealed, minefield, r, c)


def draw_grid(screen, revealed):
    for row in range(DIM):
        for col in range(DIM):
            rect = pygame.Rect(col * CELL_SIZE, row *
                               CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(
                screen, GRAY if revealed[row, col] else WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
            if revealed[row, col]:
                if minefield[row, col] == -1:
                    pygame.draw.circle(
                        screen, RED, rect.center, CELL_SIZE // 4)
                else:
                    count = count_adjacent_mines(minefield, row, col)
                    if count > 0:
                        text = font.render(str(count), True, BLUE)
                        screen.blit(text, text.get_rect(center=rect.center))


DIM = 10
NUM_MINES = 15
CELL_SIZE = 40
WIDTH, HEIGHT = DIM * CELL_SIZE, DIM * CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(None, 24)

minefield = create_minefield(DIM, NUM_MINES)
print(minefield)
minefield_count = create_adjacent_count_minefield(minefield)
revealed = np.zeros((DIM, DIM), dtype=bool)

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            row, col = y // CELL_SIZE, x // CELL_SIZE
            if not revealed[row, col]:
                reveal_cell(revealed, minefield_count, row, col)
                if minefield[row, col] == -1:
                    running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            x, y = event.pos
            row, col = y // CELL_SIZE, x // CELL_SIZE
    screen.fill(WHITE)
    draw_grid(screen, revealed)
    pygame.display.flip()

game_over_text = font.render("Game Over !", True, BLACK, RED)
game_over_rect = game_over_text.get_rect(
    center=(WIDTH//2, HEIGHT//2))
screen.blit(game_over_text, (0, 0))
pygame.time.delay(1000)
pygame.quit()
sys.exit()
