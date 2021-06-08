# Controls
# B = Pencil (Draw walls which cannot be traversed)
# E = Eraser (Erase walls)
# C = Clear all (Erase all walls)
# F = Find and colour components
# R = Stop finding components and resume drawing

import pygame
import random

pygame.init()
gameWindow = pygame.display.set_mode((720, 720))
font = pygame.font.SysFont("Arial Rounded MT Bold", 70)
colours = [
    (255, 255, 255),
    (   0,  0,   0),
    (128, 128, 128)
]
clock = pygame.time.Clock()

def drawGrid():
    for i in range(0, 744, 24):
        pygame.draw.line(gameWindow, colours[1], (i, 0), (i, 720), 2)
        pygame.draw.line(gameWindow, colours[1], (0, i), (720, i), 2)

def drawFloor(floor):
    for i in range(30):
        for j in range (30):
            pygame.draw.rect(gameWindow, colours[floor[i][j]], (j*24, i*24, j*24+24, i*24+24))

def findStart(floor):
    for i in range(30):
        for j in range (30):
            if (floor[i][j] == 0): 
                return (i, j)
    return False

def copy(floor, prefloor):
    for i in range (30):
        for j in range (30):
            prefloor[i][j] = floor[i][j]
    return (prefloor)

floor = [[0 for i in range (30)] for j in range (30)]
preFloor = [[0 for i in range (30)] for j in range (30)]
draw = True
pencil = True
search = [(-1, 0),(1, 0),(0, -1),(0, 1)]
queue = []
control = True
components = 0
c = 2

while True:
    gameWindow.fill(colours[0])
    pygame.event.clear()
    clock.tick(60)
    pygame.event.get()
    keys = pygame.key.get_pressed()

    drawFloor(floor)
    drawGrid()

    click = pygame.mouse.get_pressed()
    if (control):
        if (draw):
            if (keys[pygame.K_b]): pencil = True
            elif (keys[pygame.K_e]): pencil = False
            if (click[0] == True):
                mouseY,mouseX= pygame.mouse.get_pos()
                if (pencil): floor[mouseX//24][mouseY//24] = 1 
                else: floor[mouseX//24][mouseY//24] = 0
            if (keys[pygame.K_f]): 
                preFloor = copy(floor, preFloor)
                draw = False
        else:
            if (keys[pygame.K_r]): 
                draw, pencil, queue, control, components = True, True, [], True, 0
                floor = copy(preFloor, floor)
            if (len(queue) == 0):
                d = findStart(floor)
                if (d == False): control = False
                queue = [d]
                col = (0, 0, 0)
                while col in colours:
                    col = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                colours.append(col)
                c += 1
                if (control): components += 1
            else:
                # pop 0 for breadth first search
                tile = queue.pop(-1) 
                floor[tile[0]][tile[1]] = c
                for i in search:
                    x, y = tile[0]+i[0], tile[1]+i[1]
                    if (x < 0 or y < 0 or x >= 30 or y >= 30): continue
                    if (floor[x][y] != 0): continue
                    queue.append((x, y))
                    floor[x][y] = 2
    else:
        pygame.draw.rect(gameWindow, colours[0], (5, 615, 620, 100))
        pygame.draw.rect(gameWindow, colours[1], (10, 620, 610, 90))
        pygame.draw.rect(gameWindow, (64,63,69), (20, 630, 590, 70))
        if (components != 1): gameWindow.blit(font.render(("There are " + str(components) + " components"), 1, colours[0]) ,(30,640))
        else: gameWindow.blit(font.render(("There is " + str(components) + " component"), 1, colours[0]) ,(30,640))

    if (keys[pygame.K_c]):
        floor = [[0 for i in range (30)] for j in range (30)]
        draw, pencil, queue, control, components, c = True, True, [], True, 0, 2
        colours = [
            (255, 255, 255),
            (  0,   0,   0),
            (128, 128, 128)
        ]
    if (keys[pygame.K_r]): 
        draw, pencil, queue, control, components, c = True, True, [], True, 0, 2
        floor = copy(preFloor, floor)
        colours = [
            (255, 255, 255),
            (   0,  0,   0),
            (128, 128, 128)
        ]
    pygame.display.update()
    if (keys[pygame.K_ESCAPE]): break