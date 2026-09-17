import pygame, sys, random, math
from pygame.locals import *
from entities import *
pygame.init()
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (122, 122, 122)
DARKGREY = (100, 100, 100)
GREEN = (25, 95, 0)
LIGHTGREEN = (25, 225, 0)
CREAM = (220, 216, 130)
RED = (195, 5, 5)
BLUE = (0, 0, 255)
fontSmall = pygame.font.SysFont('monospace', 20)
fontLarge = pygame.font.SysFont('monospace', 40)

#Checks if the player is overlapping any objects that will change state. If they are, it won't change, otherwise it will
def changeState(state, entities, grid, player):
    playerDimensions = player.getDimensions()
    changeable = True
    for entity in entities:
        if entity.isChanging():
            cellX, cellY = entity.getPosition()
            cell = grid[cellX][cellY]
            if cell.playerIsInCell(playerDimensions, 1):
                changeable = False
    if changeable:
        state = not state
    return state

#Creates a 2D array of cell objects
def makeBoard():
    grid = []
    for x in range(0, round(WIDTH / 50)):
        column = []
        for y in range(0, round(HEIGHT / 50)):
            column.append(Cell(x * 50, y * 50))
        grid.append(column)
    return grid

HEIGHT = 600
WIDTH = 600
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Game Jam')
windowSurface.fill(WHITE)

frameRate = 50
grid = makeBoard()
left = False
right = False
up = False
down = False
colour = True
player = Player()
wall = Wall(6, 6, grid)
ice = Ice(6, 4, grid)
spikes = Spikes(8, 6, grid)
entities = [wall, ice, spikes]
state = True
stateChange = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                left = True
            elif event.key == K_RIGHT:
                right = True
            elif event.key == K_UP:
                up = True
            elif event.key == K_DOWN:
                down = True
            elif event.key == K_SPACE:
                stateChange = True
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                left = False
            elif event.key == K_RIGHT:
                right = False
            elif event.key == K_UP:
                up = False
            elif event.key == K_DOWN:
                down = False
    player.update(left, right, up, down, grid)
    if stateChange:
        state = changeState(state, entities, grid, player)
        stateChange = False
    for column in grid:
        for cell in column:
            cell.update(state)
            cellDimensions = cell.getDimensions()
            cellColour = cell.getColour()
            pygame.draw.rect(windowSurface, cellColour, (cellDimensions['left'], cellDimensions['top'], 50, 50))
    playerDimensions = player.getDimensions()
    pygame.draw.rect(windowSurface, GREEN, (playerDimensions['left'], playerDimensions['top'], 40, 40))
    pygame.display.update()
    clock.tick(frameRate)