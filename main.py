import pygame
import numpy as np
from pygame.locals import *


DIM = 10
NUM_MINES = 20
CELL_SIZE = 35
WIDTH, HEIGHT = DIM * CELL_SIZE+50, DIM * CELL_SIZE+200
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
LIME = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAROON = (128, 0, 0)
GREEN = (0, 128, 0)
NAVY = (0, 0, 128)
TEAL = (0, 128, 128)
PINK = (255, 0, 255)
DARK_GRAY = (128, 128, 128)
DIFFICULTY = {"Easy": 0, "Medium": 1, "Hard": 2}
CURRENT_DIFFICULTY = 1


def create_minefield(dim: int = DIM, num_mines: int = NUM_MINES):
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


def reveal_cell(revealed: np.ndarray, minefield: np.ndarray, row: int = DIM, col: int = DIM):
    '''Reveals adjacent cells of the cell [row,col] if they contain 0'''
    if not revealed[row, col] and not flagged[row, col]:
        revealed[row, col] = True
        if minefield[row, col] == 0:
            for r in range(max(0, row-1), min(DIM, row+2)):
                for c in range(max(0, col-1), min(DIM, col+2)):
                    reveal_cell(revealed, minefield, r, c)


def check_end(revealed: np.ndarray):
    count_cells_revealed = 0
    for r in range(DIM):
        for c in range(DIM):
            if revealed[r, c]:
                count_cells_revealed += 1
    if count_cells_revealed == DIM**2-NUM_MINES:
        pygame.draw.rect(screen, BLACK, win_rect_bg, 0, 25)
        screen.blit(win, win_rect)
        pygame.display.update()
        pygame.mixer_music.stop()
        win_sound.play()
        pygame.time.wait(3000)
        return True
    return False


def update_timer(revealed: np.ndarray):
    if revealed.any():
        time = (pygame.time.get_ticks() - t0)//1000
    else:
        time = 0
    timer = font.render(str(time), True, RED)
    timer_rect = timer.get_rect()
    timer_rect.right = black_bg.left + 60-4
    timer_rect.top = black_bg.top + 2
    screen.blit(timer, timer_rect)


def update_mines_left(flagged: np.ndarray, row: int = DIM, col: int = DIM):
    if flagged[row, col]:
        return 1
    else:
        return -1


def update_difficulty(code: int, dif: int):
    if (code == 1 and dif == 0) or (code == -1 and dif == 2):
        return 1
    elif code == -1:
        return 0
    elif code == 1:
        return 2


def reset(code: int = 0):
    if code == 1:   # Reprise de partie après défaite
        pygame.mixer_music.play(-1)
    first_click = True
    count_mines_left = NUM_MINES
    minefield = create_minefield(DIM, NUM_MINES)
    minefield_count = create_adjacent_count_minefield(minefield)
    revealed = np.zeros((DIM, DIM), dtype=bool)
    flagged = np.zeros((DIM, DIM), dtype=bool)
    diff = [k for (k, val) in DIFFICULTY.items() if val == CURRENT_DIFFICULTY]
    diff = font.render(diff[0], True, BLACK)
    diff_rect = diff.get_rect()
    diff_rect.left = (WIDTH-diff_rect.w)//2
    diff_rect.top = 125
    return first_click, count_mines_left, minefield, minefield_count, revealed, flagged, diff, diff_rect


def draw_grid(screen: pygame.Surface, revealed: np.ndarray):
    '''Draw minefield grid and numbers'''
    for row in range(DIM):
        for col in range(DIM):
            rect = pygame.Rect(col * CELL_SIZE+25, row *
                               CELL_SIZE+175, CELL_SIZE, CELL_SIZE)
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


pygame.init()

pygame.mixer.init()
pygame.mixer_music.load("./Ressources/Jaunter-TheSearch.mp3")
pygame.mixer_music.set_volume(0.5)
pygame.mixer_music.play(-1)
game_over = pygame.mixer.Sound("./Ressources/game_over.mp3")
game_over.set_volume(0.5)
win_sound = pygame.mixer.Sound("./Ressources/win.mp3")
win_sound.set_volume(0.5)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
icon = pygame.image.load("./Ressources/logo.png")
pygame.display.set_caption("Minesweeper")
pygame.display.set_icon(icon)
font = pygame.font.Font(None, 33)
first_click = True
count_mines_left = NUM_MINES

minefield = create_minefield(DIM, NUM_MINES)
minefield_count = create_adjacent_count_minefield(minefield)
revealed = np.zeros((DIM, DIM), dtype=bool)
flagged = np.zeros((DIM, DIM), dtype=bool)

black_bg = pygame.rect.Rect(25, 25, WIDTH - 50, 24)
white_bg = pygame.rect.Rect(85, 25, WIDTH-50-120, 24)

right_arrow = pygame.image.load("./Ressources/right_arrow.png").convert_alpha()
right_arrow = pygame.transform.scale(right_arrow, (60, 20))
right_arrow_rect = right_arrow.get_rect()
right_arrow_rect.right = WIDTH-50
right_arrow_rect.top = 125
left_arrow = pygame.image.load("./Ressources/left_arrow.png").convert_alpha()
left_arrow = pygame.transform.scale(left_arrow, (60, 20))
left_arrow_rect = left_arrow.get_rect()
left_arrow_rect.left = 50
left_arrow_rect.top = 125

diff = [k for (k, val) in DIFFICULTY.items() if val == CURRENT_DIFFICULTY]
diff = font.render(diff[0], True, BLACK)
diff_rect = diff.get_rect()
diff_rect.left = (WIDTH-diff_rect.w)//2
diff_rect.top = 125

reset_game = pygame.rect.Rect(WIDTH//2-25, 50, 50, 50)

go = font.render("Game Over !", True, RED)
go_rect_bg = pygame.rect.Rect(WIDTH//4, HEIGHT//2-25, WIDTH//2, 50)
go_rect = go.get_rect()
go_rect.left = go_rect_bg.left + (go_rect_bg.w - go_rect.w)//2
go_rect.top = go_rect_bg.top + (go_rect_bg.h - go_rect.h)//2

win = font.render("Good job !", True, LIME)
win_rect_bg = pygame.rect.Rect(WIDTH//4, HEIGHT//2-25, WIDTH//2, 50)
win_rect = win.get_rect()
win_rect.left = win_rect_bg.left + (win_rect_bg.w - win_rect.w)//2
win_rect.top = win_rect_bg.top + (win_rect_bg.h - win_rect.h)//2

# Boucle principale du jeu
running = True
while running and not check_end(revealed):
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            previous_diff = CURRENT_DIFFICULTY
            row, col = (y-175) // CELL_SIZE, (x-25) // CELL_SIZE
            if reset_game.collidepoint(x, y):
                first_click, count_mines_left, minefield, minefield_count, revealed, flagged, diff, diff_rect = reset()
            elif left_arrow_rect.collidepoint(x, y):
                CURRENT_DIFFICULTY = update_difficulty(-1, CURRENT_DIFFICULTY)
            elif right_arrow_rect.collidepoint(x, y):
                CURRENT_DIFFICULTY = update_difficulty(1, CURRENT_DIFFICULTY)
            if CURRENT_DIFFICULTY != previous_diff:
                match CURRENT_DIFFICULTY:
                    case 0:
                        NUM_MINES = 15
                    case 1:
                        NUM_MINES = 20
                    case 2:
                        NUM_MINES = 30
                first_click, count_mines_left, minefield, minefield_count, revealed, flagged, diff, diff_rect = reset()
            if row >= 0 and row < DIM and col >= 0 and col < DIM:
                if first_click:
                    t0 = pygame.time.get_ticks()
                    first_click = False
                if event.button == 1 and not revealed[row, col] and not flagged[row, col]:
                    reveal_cell(revealed, minefield_count, row, col)
                    draw_grid(screen, revealed)
                    if minefield[row, col] == -1:
                        pygame.mixer_music.stop()
                        game_over.play()
                        while not reset_game.collidepoint(x, y):
                            pygame.draw.rect(screen, BLACK, go_rect_bg, 0, 25)
                            screen.blit(go, go_rect)
                            events = pygame.event.get()
                            for event in events:
                                if event.type == QUIT:
                                    running = False
                                    quit()
                                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                                    x, y = event.pos
                            pygame.display.update()
                        first_click, count_mines_left, minefield, minefield_count, revealed, flagged, diff, diff_rect = reset(
                            1)
                elif event.button == 3 and not revealed[row, col]:
                    count_mines_left += update_mines_left(flagged, row, col)
                    if count_mines_left > 0:
                        flagged[row, col] = not flagged[row, col]
                    elif count_mines_left == 0:
                        flagged[row, col] = not flagged[row, col]
                    elif count_mines_left < 0:
                        count_mines_left = 0

    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, black_bg)
    pygame.draw.rect(screen, WHITE, white_bg)
    pygame.draw.rect(screen, GRAY, reset_game, 0, 25)
    pygame.draw.circle(screen, YELLOW, reset_game.center, 50//2.7)
    mines_left = font.render(str(count_mines_left), True, RED)
    mines_left_rect = mines_left.get_rect()
    mines_left_rect.left = black_bg.left + black_bg.w - mines_left_rect.w-4
    mines_left_rect.top = black_bg.top + 2
    screen.blit(mines_left, mines_left_rect)
    screen.blit(right_arrow, right_arrow_rect)
    screen.blit(left_arrow, left_arrow_rect)
    screen.blit(diff, diff_rect)
    update_timer(revealed)
    draw_grid(screen, revealed)
    pygame.display.flip()
