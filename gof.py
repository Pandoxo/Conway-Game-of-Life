import os
from copy import deepcopy

import pygame as pg

WIDTH, HEIGHT = 1280, 1280
WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
ROWS = 40
COLLS = ROWS
CELL_SIZE = WIDTH // COLLS

TICKS = 160
# Text
pg.font.init()
pg.init()
FONT = pg.font.SysFont("arial", 40)


pg.display.set_caption("Conway Game of Life")


def draw_board(board, gen):
    WINDOW.fill("#808080")

    color = "black"
    for i in range(ROWS):
        for j in range(COLLS):
            if board[i][j]:
                color = "yellow"
            else:
                color = "black"
            pg.draw.rect(
                WINDOW,
                color,
                [i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1],
            )

    generation = FONT.render(f"generation: {gen}", 1, "white")
    WINDOW.blit(generation, (0, 0))
    pg.display.update()


def next_state(row, col, board):
    cTc = [-1, 0, 1, -1, 1, -1, 0, 1]
    rTc = [-1, -1, -1, 0, 0, 1, 1, 1]
    live_n = 0
    state = board[row][col]
    for k in range(8):
        if board[row + rTc[k]][col + cTc[k]]:
            live_n += 1
    if state:
        if live_n < 2:
            return False
        elif live_n < 4:
            return True
        else:
            return False
    else:
        if live_n == 3:
            return True


def next_gen(board):
    global ROWS
    global COLLS
    new_board = [[False for i in range(COLLS)] for j in range(ROWS)]
    for i in range(1, ROWS - 1):
        for j in range(1, COLLS - 1):
            new_board[i][j] = next_state(i, j, board)
    return new_board


def main():
    running = True
    edit = True
    sim = False
    time_elapsed = 0
    gen = 0
    population = 0

    clock = pg.time.Clock()
    BOARD_EDIT = [[False for i in range(COLLS)] for j in range(ROWS)]
    BOARD_SIM = deepcopy(BOARD_EDIT)

    while running:

        dt = clock.tick()
        time_elapsed += dt
        if edit:
            if pg.mouse.get_pressed()[0]:
                mouse_pos = pg.mouse.get_pos()
                row = mouse_pos[0] // CELL_SIZE
                col = mouse_pos[1] // CELL_SIZE
                BOARD_EDIT[row][col] = True
            if pg.mouse.get_pressed()[2]:
                mouse_pos = pg.mouse.get_pos()
                row = mouse_pos[0] // CELL_SIZE
                col = mouse_pos[1] // CELL_SIZE
                BOARD_EDIT[row][col] = False
            draw_board(BOARD_EDIT, 0)
        elif sim:

            if time_elapsed > TICKS:
                BOARD_SIM = next_gen(BOARD_SIM)
                draw_board(BOARD_SIM, gen)
                time_elapsed = 0
                gen += 1

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    print(f"edit: {edit} sim: {sim}")
                    if edit:
                        BOARD_SIM = deepcopy(BOARD_EDIT)
                    edit = not edit
                    sim = not sim
                    gen = 0
                elif event.key == pg.K_BACKSPACE:
                    BOARD_EDIT = [[False for i in range(COLLS)] for j in range(ROWS)]
                elif event.key == pg.K_1:
                    gen += 1
                    BOARD_SIM = next_gen(BOARD_SIM)
                    draw_board(BOARD_SIM, gen)


if __name__ == "__main__":
    main()
