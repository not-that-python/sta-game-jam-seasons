import pygame, sys, random, math
from pygame.locals import *
pygame.init()
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (122, 122, 122)
GREEN = (25, 95, 0)
LIGHTGREEN = (25, 225, 0)
CREAM = (220, 216, 130)
RED = (195, 5, 5)
BLUE = (0, 0, 255)
fontSmall = pygame.font.SysFont('monospace', 20)
fontLarge = pygame.font.SysFont('monospace', 40)

class Cell():
    def __init__(self, xPos, yPos):
        self.__dimensions = {'left': xPos, 'right': xPos + 50, 'top': yPos, 'bottom': yPos + 50}
        self.__centreX = xPos + 25
        self.__centreY = yPos + 25
        self.__contains = None

    def getPos(self):
        return self.__centreX, self.__centreY

    def getDimensions(self):
        return self.__dimensions

    def updateContents(self, entity):
        self.__contains = entity

    def isSolid(self):
        if self.__contains != None:
            solid =  self.__contains.isSolid()
        else:
            solid = False
        return solid

    def playerIsInCell(self, playerDimensions, overlap):
        if playerDimensions['left'] <= self.__dimensions['right'] and playerDimensions['left'] >= self.__dimensions['left']:
            xOverlap = self.__dimensions['right'] - playerDimensions['left']
        elif playerDimensions['right'] <= self.__dimensions['right'] and playerDimensions['right'] >= self.__dimensions['left']:
            xOverlap = playerDimensions['right'] - self.__dimensions['left']
        else:
            xOverlap = 0
        if playerDimensions['bottom'] >= self.__dimensions['top'] and playerDimensions['bottom'] <= self.__dimensions['bottom']:
            yOverlap = playerDimensions['bottom'] - self.__dimensions['top']
        elif playerDimensions['top'] <= self.__dimensions['bottom'] and playerDimensions['top'] >= self.__dimensions['top']:
            yOverlap = self.__dimensions['bottom'] - playerDimensions['top']
        else:
            yOverlap = 0
        if xOverlap >= overlap and yOverlap >= overlap:
            overlapping = True
        else:
            overlapping = False
        return overlapping

    def update(self, state):
        if self.__contains != None:
            self.__contains.update(state)

    def draw(self):
        if self.__contains == None:
            pygame.draw.rect(windowSurface, CREAM, (self.__dimensions['left'], self.__dimensions['top'], 50, 50))
        else:
            pygame.draw.rect(windowSurface, self.__contains.getColour(), (self.__dimensions['left'], self.__dimensions['top'], 50, 50))

class Entity():
    def __init__(self, x, y, grid, colour, solid, hazard, damaging, changeable):
        grid[x][y].updateContents(self)
        self._x = x
        self._y = y
        self._colour = colour
        self._solid = solid
        self._hazard = hazard
        self._damaging = damaging
        self._changeable = changeable

    def isSolid(self):
        return self._solid

    def isHazard(self):
        return self._hazard

    def isDamaging(self):
        return self._damaging

    def getColour(self):
        return self._colour

    def getPosition(self):
        return self._x, self._y

    def isChanging(self):
        return self._changeable

    def update(self, state):
        pass

class Wall(Entity):
    def __init__(self, x, y, grid):
        super().__init__(x, y, grid, BLACK, True, False, False, False)

class Ice(Entity):
    def __init__(self, x, y, grid):
        super().__init__(x, y, grid, BLUE, True, False, False, True)

    def update(self, state):
        if state:
            self._solid = True
            self._colour = BLUE
        else:
            self._solid = False
            self._colour = GREY

class Player():
    def __init__(self):
        self.__dimensions = {'left': 0, 'right': 50, 'top': 0, 'bottom': 50}
        self.__centreX = 25
        self.__centreY = 25
        self.__xSpeed = 0
        self.__ySpeed = 0
        self.__speed = 5

    def update(self, left, right, up, down, grid):
        self.__xSpeed = 0
        self.__ySpeed = 0
        if left:
            self.__xSpeed -= self.__speed
        if right:
            self.__xSpeed += self.__speed
        if up:
            self.__ySpeed -= self.__speed
        if down:
            self.__ySpeed += self.__speed
        if self.__xSpeed != 0 and self.__ySpeed != 0:
            self.__xSpeed *= math.sqrt(2)/2
            self.__ySpeed *= math.sqrt(2)/2
        self.__centreX += self.__xSpeed
        self.__centreY += self.__ySpeed
        if self.__centreX > WIDTH - 25:
            self.__centreX = WIDTH - 25
        elif self.__centreX < 25:
            self.__centreX = 25
        if self.__centreY > HEIGHT - 25:
            self.__centreY = HEIGHT - 25
        elif self.__centreY < 25:
            self.__centreY = 25
        self.updateDimensions(self.__centreX, self.__centreY)
        for x in grid:
            for cell in x:
                if cell.playerIsInCell(self.__dimensions, 3):
                    if cell.isSolid():
                        if self.__xSpeed > 0:
                            x = 1
                        elif self.__xSpeed < 0:
                            x = -1
                        else:
                            x = 0
                        if self.__ySpeed > 0:
                            y = 1
                        elif self.__ySpeed < 0:
                            y = -1
                        else:
                            y = 0
                        self.positionCorrect(x, y, cell)

    def positionCorrect(self, x, y, cell):
        if x == 0 or y == 0:
            overlapping = True
            while overlapping:
                self.__centreX -= x
                self.__centreY -= y
                self.updateDimensions(self.__centreX, self.__centreY)
                if not cell.playerIsInCell(self.__dimensions, 1):
                    overlapping = False
        else:
            cellDimensions = cell.getDimensions()
            if x > 0:
                xOverlap = self.__dimensions['right'] - cellDimensions['left']
            else:
                xOverlap = cellDimensions['right'] - self.__dimensions['left']
            if y > 0:
                yOverlap = self.__dimensions['bottom'] - cellDimensions['top']
            else:
                yOverlap = cellDimensions['bottom'] - self.__dimensions['top']
            if xOverlap > yOverlap:
                self.positionCorrect(0, y, cell)
            else:
                self.positionCorrect(x, 0, cell)

    def updateDimensions(self, x, y):
        self.__dimensions['left'] = x - 25
        self.__dimensions['right'] = x + 25
        self.__dimensions['top'] = y - 25
        self.__dimensions['bottom'] = y + 25

    def getDimensions(self):
        return self.__dimensions

    def draw(self):
        pygame.draw.rect(windowSurface, GREEN, (self.__dimensions['left'], self.__dimensions['top'], 50, 50))

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
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
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
ice = Ice(8, 4, grid)
entities = [wall, ice]
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
            cell.draw()
            colour = not colour
        colour = not colour
    player.draw()
    pygame.display.update()
    clock.tick(frameRate)