import pygame, random
from constants import BLUISH, BEIGE, GOLDEN, SHADE


# клас, який відповідає за все, що відбувається на полі гри
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
        self.__lock()
        self.files = self.fileInput()

    # намалювати порожнє поле гри
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

    # перевірити чи знаходиться курсор мишки над полем гри
    def isOnTheGrid(self, MOUSE_POS):
        if MOUSE_POS[0] in range(self.x, self.x + self.width) and MOUSE_POS[1] in range(self.y, self.y + self.height):
            return [(MOUSE_POS[0] - self.x) // self.step, (MOUSE_POS[1] - self.y) // self.step]
        return False

    # виділяти сірим кольором вибрану клітинку
    def highlightCells(self, SCREEN, position, color):
        pygame.draw.rect(SCREEN, color,
                         ((position[0] * self.step) + self.x, (position[1] * self.step) + self.y, self.step, self.step))

    # стоврити колекцію початково заповнених клітинок та початково незаповнених
    def __lock(self):
        for yidx, row in enumerate(self.unsolvedGrid):
            for xidx, num in enumerate(row):
                if num != 0:
                    self.lockedCells.append([xidx, yidx])
                else:
                    self.startEmptyCells.append([xidx, yidx])

    # запис у файл початкового поля та матриці рішень
    def fileInput(self):
        code = self.boardToCode(self.unsolvedGrid)
        cd = self.boardToCode(self.solvedGrid)
        return code, cd

    # перетворення матриці у стрічку значень кожного елементу
    def boardToCode(self, brd):
        code = ''
        for row in range(9):
            for col in range(9):
                code += str(brd[row][col])
        return code

    # створення лісту поточно незаповненних клітинок
    def notComplettedCells(self, code):
        self.notCompletedCells = []
        for yidx, row in enumerate(code):
            for xidx, num in enumerate(row):
                if num == 0:
                    self.notCompletedCells.append([xidx, yidx])
        return self.notCompletedCells

    # функція перевірки на коректність деякого значення на деякій позиції
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

    # функція логічного знаходження найбільш вакантної позиції для виводу підказки
    def solve(self, board):
        correctEmptyCells = []
        correct_board = []
        for i in range(9):
            lst = []
            for j in range(9):
                if board[i][j] == self.solvedGrid[i][j]:
                    lst.append(board[i][j])
                else:
                    correctEmptyCells.append([j, i])
                    lst.append(0)
            correct_board.append(lst)
        if correct_board == self.solvedGrid:
            # print(correct_board)
            # print(self.solvedGrid)
            return None
        num_amn = []
        '''if len(self.startEmptyCells) == 0:
            rand = random.choice(self.startEmptyCells)
            self.hint_amount += 1
            return rand
        else:'''
        for i in range(len(correctEmptyCells)):
            _row, _col = correctEmptyCells[i]
            for n in range(1, 10):
                if self.checkSpace(n, (_col, _row), correct_board):
                    num_amn.append(n)
            if len(num_amn) > 1 or len(num_amn) == 0:
                num_amn = []
            elif len(num_amn) == 1:
                board[_col][_row] = num_amn[0]
                self.hint_amount += 1
                correctEmptyCells.remove([_row, _col])
                return [_row, _col]
            '''elif len(num_amn) == 0 and len(self.startEmptyCells) > 0:
                    rand = random.choice(self.startEmptyCells)
                    self.hint_amount += 1
                    return rand'''

    # зафарбування початково даних значень сірим кольором
    def shadeCells(self, SCREEN):
        for cell in self.lockedCells:
            pygame.draw.rect(SCREEN, SHADE,
                             (cell[0] * self.step + self.x, cell[1] * self.step + self.y, self.step, self.step))

    # зафарбування деяких клітинок деяким кольором
    def colorCells(self, SCREEN, color, solvedCells):
        for cell in solvedCells:
            pygame.draw.rect(SCREEN, color,
                             (cell[0] * self.step + self.x, cell[1] * self.step + self.y, self.step, self.step))

    # виділення позиції виводу підказки зеленим кольором
    def hint(self, SCREEN, position, code):
        for pos in position:
            code[pos[1]][pos[0]] = self.solvedGrid[pos[1]][pos[0]]
            self.unsolvedGrid[pos[1]][pos[0]] = self.solvedGrid[pos[1]][pos[0]]
            pygame.draw.rect(SCREEN, "#65C793",
                             (pos[0] * self.step + self.x, pos[1] * self.step + self.y, self.step, self.step))

    # ініціалізація розміру та шрифту цифр
    def __numbers(self, SCREEN, number, position):
        fnt = pygame.font.Font("assets/arial.ttf", 45)
        num = fnt.render(number, True, BLUISH)
        SCREEN.blit(num, position)

    # вивід на екран чисел
    def drawNumbers(self, SCREEN, code):
        for yidx, row in enumerate(code):
            for xidx, num in enumerate(row):
                if num != 0:
                    position = [xidx * self.step + self.x + self.step // 4, yidx * self.step + self.y]
                    self.__numbers(SCREEN, str(num), position)
