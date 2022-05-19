import pygame, sys, random, copy, functools
from constants import BLUISH, BEIGE, GOLDEN, DARK_BEIGE, SHADE

class Grid:
    def __init__(self, SCREEN, numbers, x, y):
        self.SCREEN = SCREEN
        self.x = x
        self.y = y
        self.height = 450
        self.width = 450
        self.step = 50
        self.lockedCells = []
        self.solvedCells = []
        self.solvedGrid = numbers[3]
        self.unsolvedGrid = numbers[2]
        self.hint_amount = 0
        self.notCompletedCells = []
        self.lock()



    def draw_grid(self):
        pygame.draw.rect(self.SCREEN, BLUISH, pygame.Rect(self.x, self.y, self.height, self.width), 2)

        for x in range(self.x + self.step, self.x + self.width - self.step + 1, self.step):
            if x == self.x + 3*self.step or x == self.x + self.width - 3*self.step:
                pygame.draw.line(self.SCREEN, BLUISH, (x, self.y), (x, self.y + self.height - 1), 2)
            else:
                pygame.draw.line(self.SCREEN, BLUISH, (x, self.y), (x, self.y + self.height - 1), 1)
        for y in range(self.y + self.step, self.y + self.height - self.step + 1, self.step):
            if y == self.y + 3*self.step or y == self.y + self.height - 3*self.step:
                pygame.draw.line(self.SCREEN, BLUISH, (self.x, y), (self.x + self.width - 1, y), 2)
            else:
                pygame.draw.line(self.SCREEN, BLUISH, (self.x, y), (self.x + self.width - 1, y), 1)

    def isOnTheGrid(self, MOUSE_POS):
        if MOUSE_POS[0] in range(self.x, self.x + self.width) and MOUSE_POS[1] in range(self.y, self.y + self.height):
            return ([(MOUSE_POS[0] - self.x)//self.step, (MOUSE_POS[1] - self.y)//self.step])
        return False

    def highlightCells(self, SCREEN, position, color):
        pygame.draw.rect(SCREEN, color, ((position[0]*self.step) + self.x , (position[1]*self.step) + self.y, self.step, self.step))

    def lock(self):
        for yidx, row in enumerate(self.unsolvedGrid):
            for xidx, num in enumerate(row):
                if num!=0:
                    self.lockedCells.append([xidx, yidx])
                else:
                    self.solvedCells.append([xidx, yidx])

    def notComplettedCells(self, code):
        self.notCompletedCells = []
        for yidx, row in enumerate(code):
            for xidx, num in enumerate(row):
                if num==0:
                    self.notCompletedCells.append([xidx, yidx])
        return self.notCompletedCells


    def shadeCells(self, SCREEN):
        for cell in self.lockedCells:
            pygame.draw.rect(SCREEN, SHADE, (cell[0]*self.step + self.x, cell[1]*self.step + self.y, self.step, self.step))

    def colorCells(self, SCREEN, color, solvedCells):
        for cell in solvedCells:
            pygame.draw.rect(SCREEN, color, (cell[0]*self.step + self.x, cell[1]*self.step + self.y, self.step, self.step))

    def notUsed(self, code):
        notUsedNumbers = []
        for yidx, row in enumerate(code):
            for xidx, num in enumerate(row):
                if num == 0:
                    notUsedNumbers.append([xidx, yidx])
        self.hint_amount += 1
        return random.choice(notUsedNumbers)

    def hint(self, SCREEN, position):
        for pos in position:
            self.unsolvedGrid[pos[1]][pos[0]] = self.solvedGrid[pos[1]][pos[0]]
            pygame.draw.rect(SCREEN, "#65C793", (pos[0]*self.step + self.x, pos[1]*self.step + self.y, self.step, self.step))


    def numbers(self, SCREEN, number, position):
        fnt = pygame.font.Font("assets/arial.ttf", 45)
        num = fnt.render(number, True, BLUISH)
        SCREEN.blit(num, position)

    def drawNumbers(self, SCREEN, code):
        for yidx, row in enumerate(code):
            for xidx, num in enumerate(row):
                if num != 0:
                    position = [xidx*self.step + self.x + self.step//4, yidx*self.step + self.y]
                    self.numbers(SCREEN, str(num), position)
