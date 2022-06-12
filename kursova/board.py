import random, copy


# клас, який відповідає за головний алгоритм гри та її логіку
class Board:
    def __init__(self, code=None):
        self.__resetBoard()

    # перетворює матрицю значень на стрічку коду
    def boardToCode(self, input_board=None):
        if input_board:
            _code = ''.join([str(i) for j in input_board for i in j])
            return _code
        else:
            self.code = ''.join([str(i) for j in self.board for i in j])
            return self.code

    # знаходить позицію першго нульового елементу матриці
    def findEmptyBox(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] == 0:
                    return row, col

        return False

    # перевіряє чи деяке число(від 1 до 9) підходить на деяку позицію матриці
    def checkBox(self, num, position):
        if not self.board[position[0]][position[1]] == 0:  # перевіряє чи клітинка вже заповнена
            return False

        for col in self.board[position[0]]:  # перевіряє чи є це деяке число в рядку
            if col == num:
                return False

        for row in range(len(self.board)):  # перевіряє чи є це деяке число в колонці
            if self.board[row][position[1]] == num:
                return False

        _internalBoxRow = position[0] // 3
        _internalBoxCol = position[1] // 3

        for i in range(3):  # перевіряє чи є це деяке число в меншому квадраті 3х3
            for j in range(3):
                if self.board[i + (_internalBoxRow * 3)][j + (_internalBoxCol * 3)] == num:
                    return False

        return True

    # функція рекурсивного вирішення
    def solve(self):
        _spacesAvailable = self.findEmptyBox()

        if not _spacesAvailable:
            return True
        else:
            row, col = _spacesAvailable
        for n in range(1, 10):
            if self.checkBox(n, (row, col)):
                self.board[row][col] = n

                if self.solve():
                    return self.board

                self.board[row][col] = 0

        return False

    # функція генерації початкового поля гри та матриці рішень до нього
    def createBoards(self, difficulty):
        self.board, _fullBoard = self.createStartBoard(self.__createRandomFullBoard(), difficulty)
        return self.board, _fullBoard

    # видаляє з повністю заповненої таблиці деяку кількість значень клітинок, базуючись на вибраній складності
    def createStartBoard(self, fullBoard, difficulty):
        self.board = copy.deepcopy(fullBoard)

        if difficulty == "easy":
            _squares_to_remove = 36
        elif difficulty == "medium":
            _squares_to_remove = 42
        elif difficulty == "hard":
            _squares_to_remove = 48
        else:
            return

        _counter = 0
        while _counter < 4:
            _rRow = random.randint(0, 2)
            _rCol = random.randint(0, 2)
            if self.board[_rRow][_rCol] != 0:
                self.board[_rRow][_rCol] = 0
                _counter += 1

        _counter = 0
        while _counter < 4:
            _rRow = random.randint(3, 5)
            _rCol = random.randint(3, 5)
            if self.board[_rRow][_rCol] != 0:
                self.board[_rRow][_rCol] = 0
                _counter += 1

        _counter = 0
        while _counter < 4:
            _rRow = random.randint(6, 8)
            _rCol = random.randint(6, 8)
            if self.board[_rRow][_rCol] != 0:
                self.board[_rRow][_rCol] = 0
                _counter += 1

        _squares_to_remove -= 12
        _counter = 0
        while _counter < _squares_to_remove:
            _row = random.randint(0, 8)
            _col = random.randint(0, 8)

            if self.board[_row][_col] != 0:
                n = self.board[_row][_col]
                self.board[_row][_col] = 0

                if len(self.findNumberOfSolutions()) != 1:
                    self.board[_row][_col] = n
                    continue

                _counter += 1

        return self.board, fullBoard

    # генерує повністю коректно заповену таблицю значень поля гри
    def __createRandomFullBoard(self):
        self.__resetBoard()

        _l = list(range(1, 10))
        for row in range(3):
            for col in range(3):
                _num = random.choice(_l)
                self.board[row][col] = _num
                _l.remove(_num)

        _l = list(range(1, 10))
        for row in range(3, 6):
            for col in range(3, 6):
                _num = random.choice(_l)
                self.board[row][col] = _num
                _l.remove(_num)

        _l = list(range(1, 10))
        for row in range(6, 9):
            for col in range(6, 9):
                _num = random.choice(_l)
                self.board[row][col] = _num
                _l.remove(_num)
        return self.__finishCreating()

    # функція рекурсивного догенерування повністю заповненої таблиці
    def __finishCreating(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == 0:
                    _num = random.randint(1, 9)

                    if self.checkBox(_num, (row, col)):
                        self.board[row][col] = _num

                        if self.solve():
                            self.__finishCreating()
                            return self.board

                        self.board[row][col] = 0


        return False

    # знаходить кількість рішень для деякої напівпорожньої матриці та повертає множину цих значень
    def findNumberOfSolutions(self):
        _z = 0
        _list_of_solutions = []

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == 0:
                    _z += 1

        for i in range(1, _z + 1):
            _board_copy = copy.deepcopy(self)

            _row, _col = self.__findEmptyBoxToFindNumberOfSolutions(_board_copy.board, i)
            _board_copy_solution = _board_copy.__solveToFindNumberOfSolutions(_row, _col)

            _list_of_solutions.append(self.boardToCode(input_board=_board_copy_solution))
            if len(list(set(_list_of_solutions))) > 1:
                break

        return list(set(_list_of_solutions))

    # знаходить деякий за номером нульовий елемент матриці
    def __findEmptyBoxToFindNumberOfSolutions(self, board, num):
        _k = 1
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == 0:
                    if _k == num:
                        return (row, col)

                    _k += 1

        return False

    # вирішує деякую напівпорожню матрицю задля знаходження кількості її розв'язків
    def __solveToFindNumberOfSolutions(self, row, col):
        for n in range(1, 10):
            if self.checkBox(n, (row, col)):
                self.board[row][col] = n

                if self.solve():
                    return self.board

                self.board[row][col] = 0

        return False

    # повністю обнуляє матрицю
    def __resetBoard(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        return self.board
