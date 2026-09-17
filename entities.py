import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (122, 122, 122)
DARKGREY = (75, 75, 75)
GREEN = (25, 95, 0)
LIGHTGREEN = (25, 225, 0)
CREAM = (220, 216, 130)
RED = (195, 5, 5)
BLUE = (0, 0, 255)
HEIGHT = 600
WIDTH = 600

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

    #Checks if the player is overlapping with the cell by the given number of pixels
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

    def getColour(self):
        if self.__contains == None:
            
            # checkerboard colours
            if ((self.__dimensions["left"] + self.__dimensions["top"])/50) % 2 == 0:
                colour = CREAM
            else:
                colour = WHITE
        else:
            colour = self.__contains.getColour()
        return colour

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

class Spikes(Entity):
    def __init__(self, x, y, grid):
        super().__init__(x, y, grid, DARKGREY, False, True, False, False)

class Player():
    def __init__(self):
        self.__dimensions = {'left': 0, 'right': 39, 'top': 0, 'bottom': 39}
        self.__centreX = 19.5
        self.__centreY = 19.5
        self.__xSpeed = 0
        self.__ySpeed = 0
        self.__speed = 4

    #Moves the player
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
            #Normalise the vector so diagonal movement isn't faster than normal movement
            self.__xSpeed *= math.sqrt(2)/2
            self.__ySpeed *= math.sqrt(2)/2
        self.__centreX += self.__xSpeed
        self.__centreY += self.__ySpeed
        #Stops the player from moving off the edge of the screen
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
                if cell.playerIsInCell(self.__dimensions, 2.5):
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

    #Moves the player out of a solid object
    def positionCorrect(self, x, y, cell):
        if x == 0 or y == 0:
            #Repeatedly shifts the player one pixel at a time in the given direction until they aren't overlapping
            overlapping = True
            while overlapping:
                self.__centreX -= x
                self.__centreY -= y
                self.updateDimensions(self.__centreX, self.__centreY)
                if not cell.playerIsInCell(self.__dimensions, 1):
                    overlapping = False
        else:
            #Determines the shortest overlap distance to shift the player by
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
        self.__dimensions['left'] = x - 19.5
        self.__dimensions['right'] = x + 19.5
        self.__dimensions['top'] = y - 19.5
        self.__dimensions['bottom'] = y + 19.5

    def getDimensions(self):
        return self.__dimensions