import pygame
import numpy as np
from pygame_widgets.button import Button
from pygame.locals import *
import sys


def create_minefield(dim: int = 10, num_mines: int = 15):
    '''Returns a dim x dim minefield with num_mines mines at random places'''
    field = np.zeros((dim, dim), dtype=int)
    indices = np.random.choice(dim * dim, num_mines, replace=False)
    for index in indices:
        row = index // dim
        col = index % dim
        field[row, col] = -1
    return field


def create_adjacent_count_minefield(field: np.ndarray):
    '''Returns a field's copy containing the count of adjacent mines'''
    field_copied = field.copy()
    for r in range(len(field_copied)):
        for c in range(len(field_copied[r])):
            if field_copied[r, c] != -1:
                field_copied[r, c] = count_adjacent_mines(field, r, c)
    return field_copied


def count_adjacent_mines(field: np.ndarray, row: int, col: int):
    '''Returns the number of mines within the adjacent cells of the cell [row,col]'''
    count = 0
    for r in range(max(0, row-1), min(DIM, row+2)):
        for c in range(max(0, col-1), min(DIM, col+2)):
            if field[r, c] == -1:
                count += 1
    return count


def reveal_cell(revealed: np.ndarray, minefield: np.ndarray, row: int, col: int):
    '''Reveals adjacent cells of the cell [row,col] if they contain 0'''
    if not revealed[row, col] and not flagged[row, col]:
        revealed[row, col] = True
        if minefield[row, col] == 0:
            for r in range(max(0, row-1), min(DIM, row+2)):
                for c in range(max(0, col-1), min(DIM, col+2)):
                    reveal_cell(revealed, minefield, r, c)


def draw_grid(screen: pygame.Surface, revealed: np.ndarray):
    '''Draw minefield grid and numbers'''
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
                        color = BLUE
                        match count:
                            case 2:
                                color = GREEN
                            case 3:
                                color = RED
                            case 4:
                                color = NAVY
                            case 5:
                                color = MAROON
                            case 6:
                                color = TEAL
                            case 7:
                                color = PINK
                            case 8:
                                color = DARK_GRAY
                        text = font.render(str(count), True, color)
                        screen.blit(text, text.get_rect(center=rect.center))
            elif flagged[row, col]:
                pygame.draw.circle(screen, LIME, rect.center, CELL_SIZE // 4)


DIM = 10
NUM_MINES = 15
CELL_SIZE = 40
WIDTH, HEIGHT = DIM * CELL_SIZE, DIM * CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
LIME = (0, 255, 0)
BLUE = (0, 0, 255)
MAROON = (128, 0, 0)
GREEN = (0, 128, 0)
NAVY = (0, 0, 128)
TEAL = (0, 128, 128)
PINK = (255, 0, 255)
DARK_GRAY = (128, 128, 128)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
icon = pygame.image.load("./Ressources/logo.png")
pygame.display.set_caption("Minesweeper")
pygame.display.set_icon(icon)
font = pygame.font.Font(None, 30)

minefield = create_minefield(DIM, NUM_MINES)
print(minefield)
minefield_count = create_adjacent_count_minefield(minefield)
revealed = np.zeros((DIM, DIM), dtype=bool)
flagged = np.zeros((DIM, DIM), dtype=bool)

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            row, col = y // CELL_SIZE, x // CELL_SIZE
            if not revealed[row, col] and not flagged[row, col]:
                reveal_cell(revealed, minefield_count, row, col)
                if minefield[row, col] == -1:
                    running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            x, y = event.pos
            row, col = y // CELL_SIZE, x // CELL_SIZE
            if not revealed[row, col]:
                flagged[row, col] = not flagged[row, col]

    screen.fill(WHITE)
    draw_grid(screen, revealed)
    pygame.display.flip()

pygame.quit()
sys.exit()
