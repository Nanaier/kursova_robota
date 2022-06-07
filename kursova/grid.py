import pygame, random
from constants import BLUISH, BEIGE, GOLDEN, SHADE


class Grid:
    def __init__(self, SCREEN, numbers, x, y, hint_amount=0):
        self.SCREEN = SCREEN
        self.x = x
        self.y = y
        self.height = 450
        self.width = 450
        self.step = 50
        self.lockedCells = []
        self.startEmptyCells = []
        self.solvedGrid = numbers[1]
        self.unsolvedGrid = numbers[0]
        self.hint_amount = hint_amount
        self.notCompletedCells = []
        self.lock()
        self.fileInput()

    def draw_grid(self):
        pygame.draw.rect(self.SCREEN, BLUISH, pygame.Rect(self.x, self.y, self.height, self.width), 2)

        for x in range(self.x + self.step, self.x + self.width - self.step + 1, self.step):
            if x == self.x + 3 * self.step or x == self.x + self.width - 3 * self.step:
                pygame.draw.line(self.SCREEN, BLUISH, (x, self.y), (x, self.y + self.height - 1), 2)
            else:
                pygame.draw.line(self.SCREEN, BLUISH, (x, self.y), (x, self.y + self.height - 1), 1)
        for y in range(self.y + self.step, self.y + self.height - self.step + 1, self.step):
            if y == self.y + 3 * self.step or y == self.y + self.height - 3 * self.step:
                pygame.draw.line(self.SCREEN, BLUISH, (self.x, y), (self.x + self.width - 1, y), 2)
            else:
                pygame.draw.line(self.SCREEN, BLUISH, (self.x, y), (self.x + self.width - 1, y), 1)

    def isOnTheGrid(self, MOUSE_POS):
        if MOUSE_POS[0] in range(self.x, self.x + self.width) and MOUSE_POS[1] in range(self.y, self.y + self.height):
            return [(MOUSE_POS[0] - self.x) // self.step, (MOUSE_POS[1] - self.y) // self.step]
        return False

    def highlightCells(self, SCREEN, position, color):
        pygame.draw.rect(SCREEN, color,
                         ((position[0] * self.step) + self.x, (position[1] * self.step) + self.y, self.step, self.step))

    def lock(self):
        for yidx, row in enumerate(self.unsolvedGrid):
            for xidx, num in enumerate(row):
                if num != 0:
                    self.lockedCells.append([xidx, yidx])
                else:
                    self.startEmptyCells.append([xidx, yidx])

    def fileInput(self):
        code = self.boardToCode(self.unsolvedGrid)
        cd = self.boardToCode(self.solvedGrid)
        with open("input.txt", "w") as file:
            file.write(code + '\n' + cd)

    def boardToCode(self, brd):
        code = ''
        for row in range(9):
            for col in range(9):
                code += str(brd[row][col])
        return code

    def notComplettedCells(self, code):
        self.notCompletedCells = []
        for yidx, row in enumerate(code):
            for xidx, num in enumerate(row):
                if num == 0:
                    self.notCompletedCells.append([xidx, yidx])
        return self.notCompletedCells

    def checkSpace(self, num, space, board):
        if not board[space[0]][space[1]] == 0:
            return None

        for col in board[space[0]]:
            if col == num:
                return None

        for row in range(len(board)):
            if board[row][space[1]] == num:
                return None

        _internalBoxRow = space[0] // 3
        _internalBoxCol = space[1] // 3

        for i in range(3):
            for j in range(3):
                if board[i + (_internalBoxRow * 3)][j + (_internalBoxCol * 3)] == num:
                    return None

        return num

    def solve(self, board):

        correct_board = []
        for i in range(9):
            lst = []
            for j in range(9):
                if board[i][j] == self.solvedGrid[i][j]:
                    lst.append(board[i][j])
                else:
                    lst.append(0)
            correct_board.append(lst)
        if correct_board == self.solvedGrid:
            return None
        num_amn = []
        if len(self.startEmptyCells) == 0:
            rand = random.choice(self.startEmptyCells)
            self.hint_amount += 1
            return rand
        else:
            for i in range(len(self.startEmptyCells)):
                row, col = self.startEmptyCells[i]
                for n in range(1, 10):
                    if self.checkSpace(n, (col, row), correct_board):
                        num_amn.append(n)
                if len(num_amn) > 1 or len(num_amn) == 0:
                    num_amn = []
                elif len(num_amn) == 1:
                    board[col][row] = num_amn[0]
                    self.hint_amount += 1
                    self.startEmptyCells.remove([row, col])
                    return [row, col]
                '''elif len(num_amn) == 0 and len(self.startEmptyCells) > 0:
                    rand = random.choice(self.startEmptyCells)
                    self.hint_amount += 1
                    return rand'''

    def shadeCells(self, SCREEN):
        for cell in self.lockedCells:
            pygame.draw.rect(SCREEN, SHADE,
                             (cell[0] * self.step + self.x, cell[1] * self.step + self.y, self.step, self.step))

    def colorCells(self, SCREEN, color, solvedCells):
        for cell in solvedCells:
            pygame.draw.rect(SCREEN, color,
                             (cell[0] * self.step + self.x, cell[1] * self.step + self.y, self.step, self.step))

    def hint(self, SCREEN, position, code):
        for pos in position:
            code[pos[1]][pos[0]] = self.solvedGrid[pos[1]][pos[0]]
            self.unsolvedGrid[pos[1]][pos[0]] = self.solvedGrid[pos[1]][pos[0]]
            pygame.draw.rect(SCREEN, "#65C793",
                             (pos[0] * self.step + self.x, pos[1] * self.step + self.y, self.step, self.step))

    def numbers(self, SCREEN, number, position):
        fnt = pygame.font.Font("assets/arial.ttf", 45)
        num = fnt.render(number, True, BLUISH)
        SCREEN.blit(num, position)

    def drawNumbers(self, SCREEN, code):
        for yidx, row in enumerate(code):
            for xidx, num in enumerate(row):
                if num != 0:
                    position = [xidx * self.step + self.x + self.step // 4, yidx * self.step + self.y]
                    self.numbers(SCREEN, str(num), position)
