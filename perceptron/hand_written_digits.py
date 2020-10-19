import pygame
import numpy as np
from perceptron import *
from dataset import *
# initialize the pygame module
pygame.init()

# initialize screen
screen = pygame.display.set_mode((480, 480))

# parameters of each of cells in the grid
width, height = 40, 40

# w - number of columny , h- number of rows
w, h = 5, 5
# margin of the grid
margin = 5
# colors
green = (0, 255, 0)
white = (255, 255, 255)
# grid describing what is
grid = np.zeros((h, w))
# font
font = pygame.font.Font('freesansbold.ttf', 40)
# text on buttons
text = [font.render('<', True, green,  white),
        font.render('^', True, green,  white),
        font.render('>', True, green,  white),
        font.render('v', True, green,  white),
        font.render('?', True, green,  white),
        font.render('r', True, green,  white),
        font.render('h', True, green,  white),
        font.render('v', True, green,  white),
        font.render('n', True, green,  white),
        font.render('c', True, green,  white)
        ]
# digits on button
digits = [font.render('0', True, green,  white),
          font.render('1', True, green,  white),
          font.render('2', True, green,  white),
          font.render('3', True, green,  white),
          font.render('4', True, green,  white),
          font.render('5', True, green,  white),
          font.render('6', True, green,  white),
          font.render('7', True, green,  white),
          font.render('8', True, green,  white),
          font.render('9', True, green,  white)]
# put text in rect
textRect = []
digitsRect = []
for i in range(len(text)):
    textRect.append(text[i].get_rect().move(w*(width+margin)+5, 5+45*i))
for i in range(len(digits)):
    digitsRect.append(digits[i].get_rect().move(
        (w+1)*(width+margin)+5, 5+45*i))


def move_up(grid, new_grid):
    for row in range(h):
        for column in range(w):
            new_grid[row, column] = grid[(row+1) % 5, column]
    return new_grid


def move_down(grid, new_grid):
    for row in range(h):
        for column in range(w):
            new_grid[row, column] = grid[(row-1) % 5, column]
    return new_grid


def move_right(grid, new_grid):
    for row in range(h):
        for column in range(w):
            new_grid[row, column] = grid[row, (column-1) % 5]
    return new_grid


def move_left(grid, new_grid):
    for row in range(h):
        for column in range(w):
            new_grid[row, column] = grid[row, (column+1) % 5]
    return new_grid


def move_rotation(grid, new_grid):  # rotation center is center of grid
    for row in range(h):
        for column in range(w):
            new_grid[row, column] = grid[(4-column), (row)]
    return new_grid


def neg(grid):
    for row in range(h):
        for column in range(w):
            if grid[row, column] == 0:
                grid[row, column] = 1
            else:
                grid[row, column] = 0
    return grid


def draw_digit(digit):
    # number form dataset.py
    return np.array(number[digit])


def move_draw(position, grid):
    new_grid = grid.copy()
    if position["column"] == w:
        if position["row"] == 0:
            return move_left(grid, new_grid)
        elif position['row'] == 1:
            return move_up(grid, new_grid)
        elif position['row'] == 2:
            return move_right(grid, new_grid)
        elif position['row'] == 3:
            return move_down(grid, new_grid)
        elif position['row'] == 4:
            return move_rotation(grid, new_grid)
        elif position['row'] == 5:
            # random
            pass
        elif position['row'] == 6:
            # horizontal
            pass
        elif position['row'] == 7:
            # vertical
            pass
        elif position['row'] == 8:
            return neg(grid)
        elif position['row'] == 9:
            # clear
            return np.zeros((h, w))
    if position['column'] == w+1:
        if position['row'] < 10:
            return draw_digit(position['row'])
    return grid


# main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (width + margin)
            row = pos[1] // (height + margin)

            # set position on grid
            try:
                if grid[row, column] == 0:
                    grid[row, column] = 1
                else:
                    grid[row, column] = 0
            except:
                grid = move_draw({'row': row, 'column': column}, grid.copy())

    # drawing buttons and grid
    for i in range(len(textRect)):
        screen.blit(text[i], textRect[i])
    for i in range(len(digitsRect)):
        screen.blit(digits[i], digitsRect[i])
    for row in range(h):
        for column in range(w):
            color = white
            if grid[row, column] == 1:
                color = green
            pygame.draw.rect(screen, color,
                             [(margin + width) * column + margin,
                              (margin + height) * row + margin,
                              width,
                              height])

    pygame.display.flip()

pygame.quit()
