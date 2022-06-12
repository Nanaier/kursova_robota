from board import *
from button import *
from grid import *
import os, sys
vector = pygame.math.Vector2


# клас, який відповідає за графічний інтерфейс та з'єднує логіку гри з інтерфейсом
class Screen:
    def __init__(self, screen):
        self.SCREEN = screen
        self.running = True
        self.selected = None
        self.hint_cells = []
        self.notCompletedCells = []
        self.x = 410
        self.y = 100
        self.hint_amn = 0

    @staticmethod
    def __get_font(size):  # ініціалізація шрифту за деяким розміром
        return pygame.font.Font("assets/font.ttf", size)

    # вивід деякого тексту деякого розміру на деяку позицію
    def __print_text(self, text, pos, size, color=GOLDEN):
        text = Screen.__get_font(int(size)).render(text, True, color)
        rect = text.get_rect(center=pos)
        self.SCREEN.blit(text, rect)

    # екран автоматичного вирішення судоку
    def solve_display(self, mode, game_matrix):
        self.grid = Grid(self.SCREEN, game_matrix, self.x, self.y + 40)
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            SOLVE_BACK = Button(pos=(640, 670), text_input="BACK", font=Screen.__get_font(50), base_color=BLUISH, hovering_color=GOLDEN)
            SOLVE_BACK.changeColor(mouse_pos)
            self.SCREEN.fill(BEIGE)
            SOLVE_BACK.update(self.SCREEN)
            self.grid.drawNumbers(self.SCREEN, game_matrix[1])
            self.grid.draw_grid()
            self.__print_text("Solved sudoku:", (640, 60), 50)
            self.__print_text(mode, (440, 130), 10)
            self.__print_text(str(self.hint_amn) + "/3", (840, 130), 10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if SOLVE_BACK.checkForInput(mouse_pos):
                        Screen.main_menu(self)

            pygame.display.update()

    # екран перевірки правильності рішення(фінальний екран)
    def finish_display(self, mode, game_matrix):
        self.grid = Grid(self.SCREEN, game_matrix, self.x + 300, self.y + 30)
        while self.running:
            self.SCREEN.fill(BEIGE)
            mouse_pos = pygame.mouse.get_pos()
            FINISH_DISPLAY_BACK = Button(pos=(350, 550), text_input="QUIT", font=Screen.__get_font(50), base_color=BLUISH, hovering_color=GOLDEN)
            FINISH_DISPLAY_BACK.changeColor(mouse_pos)
            FINISH_DISPLAY_BACK.update(self.SCREEN)

            self.grid.drawNumbers(self.SCREEN, game_matrix[1])
            self.grid.draw_grid()
            if game_matrix[0] == game_matrix[1]:
                self.__print_text("You've won!", (640, 60), 50)
                self.__print_text("Congratulations!", (340, 250), 35)
                self.__print_text("You used " + str(self.hint_amn) + "/3 hints", (340, 400), 35)
                self.__print_text(mode, (730, 120), 10)
            else:
                self.__print_text("You've lost(", (640, 60), 50)
                self.__print_text(mode, (730, 120), 10)
                self.__print_text(str(self.hint_amn) + "/3", (1140, 120), 10)
                self.__print_text("This was the right", (340, 250), 35)
                self.__print_text("sudoku grid:", (340, 400), 35)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if FINISH_DISPLAY_BACK.checkForInput(mouse_pos):
                        Screen.main_menu(self)
            pygame.display.update()

    # екран гри на деякій складності
    def mode_play(self, mode, file_insides):
        solve_pressed = 0
        self.hint_cells = []
        if not file_insides:
            self.hint_amn = 0
            brd = Board()
            game_matrix = brd.createBoards(mode)
            self.grid = Grid(self.SCREEN, game_matrix, self.x, self.y)
            with open("game_started.txt", "w") as file:
                file.write(self.grid.boardToCode(game_matrix[0]) + '\n' + self.grid.boardToCode(game_matrix[1]))
        else:
            game_matrix = self.__empty_code_list()
            with open("game_saved.txt", "r") as file:
                lst = file.readlines()
                game_matrix[0] = self.__codeToBoard(lst[0])
                game_matrix[1] = self.__codeToBoard(lst[1])
                cd = self.__codeToBoard(lst[2])
                self.hint_amn = int(lst[4])
                if len(lst) <= 5:
                    self.hint_cells = []
                else:
                    self.hint_cells = self.__code_to_hint_pos(lst[5])
            self.grid = Grid(self.SCREEN, game_matrix, self.x, self.y, self.hint_amn)
            game_matrix[0] = cd
        self.notCompletedCells = []
        while self.running:
            play_mouse_pos = pygame.mouse.get_pos()
            PLAY_BACK = Button(pos=(640, 670), text_input="BACK", font=Screen.__get_font(50), base_color=BLUISH, hovering_color=GOLDEN)
            PLAY_BACK.changeColor(play_mouse_pos)
            self.SCREEN.fill(BEIGE)
            PLAY_BACK.update(self.SCREEN)
            self.grid.shadeCells(self.SCREEN)
            self.grid.colorCells(self.SCREEN, '#FF6666', self.notCompletedCells)
            self.grid.hint(self.SCREEN, self.hint_cells, game_matrix[0])
            if self.selected:
                self.grid.highlightCells(self.SCREEN, self.selected, SHADE)
            self.grid.drawNumbers(self.SCREEN, game_matrix[0])
            pygame.draw.rect(self.SCREEN, BLUISH, pygame.Rect(90, 150, 240, 100))
            SOLVE_BUTTON = Button(pos=(210, 200), text_input="SOLVE", font=Screen.__get_font(45), base_color=BEIGE, hovering_color="White")

            pygame.draw.rect(self.SCREEN, BLUISH, pygame.Rect(90, 350, 240, 100))
            HINT_BUTTON = Button(pos=(210, 400), text_input="HINT", font=Screen.__get_font(45), base_color=BEIGE, hovering_color="White")

            pygame.draw.rect(self.SCREEN, BLUISH, pygame.Rect(930, 150, 240, 100))
            CHECK_BUTTON = Button(pos=(1050, 200), text_input="CHECK", font=Screen.__get_font(45), base_color=BEIGE, hovering_color="White")

            pygame.draw.rect(self.SCREEN, BLUISH, pygame.Rect(930, 350, 240, 100))
            SAVE_BUTTON = Button(pos=(1050, 400), text_input="SAVE", font=Screen.__get_font(45), base_color=BEIGE, hovering_color="White")

            for button in [SOLVE_BUTTON, HINT_BUTTON, CHECK_BUTTON, SAVE_BUTTON]:
                button.changeColor(play_mouse_pos)
                button.update(self.SCREEN)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BACK.checkForInput(play_mouse_pos):
                        Screen.main_menu(self)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if SOLVE_BUTTON.checkForInput(play_mouse_pos):
                        if file_insides is True or solve_pressed>0:
                            with open("game_saved.txt", "w") as file:
                                file.truncate()
                        Screen.solve_display(self, mode, game_matrix)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    selected = self.grid.isOnTheGrid(play_mouse_pos)
                    if selected:
                        self.selected = selected
                    else:
                        self.selected = None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if HINT_BUTTON.checkForInput(play_mouse_pos) and self.grid.hint_amount < 3:
                        temp_hint = self.grid.solve(game_matrix[0])
                        if temp_hint is None:
                            if file_insides is True or solve_pressed > 0:
                                with open("game_saved.txt", "w") as file:
                                    file.truncate()
                            Screen.finish_display(self, mode, game_matrix)
                        else:
                            self.hint_cells.append(temp_hint)
                            self.hint_amn = self.grid.hint_amount
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if CHECK_BUTTON.checkForInput(play_mouse_pos):
                        if len(self.grid.notComplettedCells(game_matrix[0])) != 0:
                            self.notCompletedCells = self.grid.notComplettedCells(game_matrix[0])
                        else:
                            if file_insides is True or solve_pressed > 0:
                                with open("game_saved.txt", "w") as file:
                                    file.truncate()
                            Screen.finish_display(self, mode, game_matrix)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if SAVE_BUTTON.checkForInput(play_mouse_pos):
                        solve_pressed+=1
                        code, cd = self.grid.files
                        with open("game_saved.txt", "w") as file:
                            file.write(code + '\n' + cd + '\n' + self.grid.boardToCode(game_matrix[0]) + '\n' + mode + '\n' + str(self.hint_amn) + '\n' + self.__hint_pos_code())
                if event.type == pygame.KEYDOWN:
                    if self.selected is not None and self.selected not in self.grid.lockedCells and self.selected not in self.hint_cells:
                        if event.unicode.isdigit():
                            game_matrix[0][self.selected[1]][self.selected[0]] = int(event.unicode)

            self.grid.draw_grid()
            self.__print_text(mode, (440, 90), 10)
            self.__print_text(str(self.hint_amn) + "/3", (840, 90), 10)
            pygame.display.update()

    # перетворення стрічки значень позицій підказок на ліст позицій
    def __code_to_hint_pos(self, code):
        hint_pos = []
        for i in range(len(code)//2):
            lst = [0, 0]
            for j in range(2):
                lst[j] = int(code[0])
                code = code[1:]
            hint_pos.append(lst)
        return hint_pos

    # функція перетворення позицій підказок на стрічку значень позицій підказок
    def __hint_pos_code(self):
        code = ''
        for i in range(0, len(self.hint_cells)):
            code += str(self.hint_cells[i][0])
            code += str(self.hint_cells[i][1])
        return code

    # екран вибору складності гри
    def play(self):
        while self.running:
            play_mouse_pos = pygame.mouse.get_pos()
            self.SCREEN.fill(BEIGE)
            self.__print_text("SELECT YOUR MODE", (640, 60), 60)
            PLAY_BACK = Button(pos=(640, 670), text_input="BACK", font=Screen.__get_font(50), base_color=BLUISH, hovering_color=GOLDEN)
            PLAY_BACK.changeColor(play_mouse_pos)
            PLAY_BACK.update(self.SCREEN)
            PLAY_EASY = Button(pos=(640, 200), text_input="EASY MODE", font=Screen.__get_font(65), base_color=BLUISH, hovering_color=GOLDEN)
            PLAY_EASY.changeColor(play_mouse_pos)
            PLAY_EASY.update(self.SCREEN)
            PLAY_MEDIUM = Button(pos=(640, 350), text_input="MEDIUM MODE", font=Screen.__get_font(65), base_color=BLUISH, hovering_color=GOLDEN)
            PLAY_MEDIUM.changeColor(play_mouse_pos)
            PLAY_MEDIUM.update(self.SCREEN)
            PLAY_HARD = Button(pos=(640, 500), text_input="HARD MODE", font=Screen.__get_font(65), base_color=BLUISH, hovering_color=GOLDEN)
            PLAY_HARD.changeColor(play_mouse_pos)
            PLAY_HARD.update(self.SCREEN)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BACK.checkForInput(play_mouse_pos):
                        Screen.main_menu(self)
                    if PLAY_EASY.checkForInput(play_mouse_pos):
                        mode = "easy"
                        Screen.mode_play(self, mode, False)
                    if PLAY_MEDIUM.checkForInput(play_mouse_pos):
                        mode = "medium"
                        Screen.mode_play(self, mode, False)
                    if PLAY_HARD.checkForInput(play_mouse_pos):
                        mode = "hard"
                        Screen.mode_play(self, mode, False)
            pygame.display.update()

    # екран головного меню
    def main_menu(self):
        while self.running:
            self.SCREEN.fill(BEIGE)
            menu_mouse_pos = pygame.mouse.get_pos()
            self.__print_text("SUDOKU", (640, 160), 150)
            if os.stat("game_saved.txt").st_size == 0:
                pygame.draw.rect(self.SCREEN, BLUISH, pygame.Rect(370, 310, 520, 170))
                pygame.draw.rect(self.SCREEN, BLUISH, pygame.Rect(460, 500, 350, 100))
                MAIN_PLAY_BUTTON = Button(pos=(640, 400), text_input="PLAY", font=Screen.__get_font(120), base_color=BEIGE, hovering_color="White")
                MAIN_QUIT_BUTTON = Button(pos=(640, 550), text_input="QUIT", font=Screen.__get_font(75), base_color=BEIGE, hovering_color="White")

                for button in [MAIN_PLAY_BUTTON, MAIN_QUIT_BUTTON]:
                    button.changeColor(menu_mouse_pos)
                    button.update(self.SCREEN)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if MAIN_PLAY_BUTTON.checkForInput(menu_mouse_pos):
                            Screen.play(self)
                        if MAIN_QUIT_BUTTON.checkForInput(menu_mouse_pos):
                            pygame.quit()
                            sys.exit()
            else:
                pygame.draw.rect(self.SCREEN, BLUISH, pygame.Rect(370, 260, 520, 170))
                pygame.draw.rect(self.SCREEN, BLUISH, pygame.Rect(460, 600, 350, 100))
                pygame.draw.rect(self.SCREEN, BLUISH, pygame.Rect(380, 460, 500, 110))
                MAIN_PLAY_BUTTON = Button(pos=(640, 350), text_input="PLAY", font=Screen.__get_font(120), base_color=BEIGE, hovering_color="White")
                MAIN_RESUME_BUTTON = Button(pos=(640, 520), text_input="RESUME", font=Screen.__get_font(80), base_color=BEIGE, hovering_color="White")
                MAIN_QUIT_BUTTON = Button(pos=(640, 650), text_input="QUIT", font=Screen.__get_font(75), base_color=BEIGE, hovering_color="White")
                for button in [MAIN_PLAY_BUTTON, MAIN_RESUME_BUTTON, MAIN_QUIT_BUTTON]:
                    button.changeColor(menu_mouse_pos)
                    button.update(self.SCREEN)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if MAIN_RESUME_BUTTON.checkForInput(menu_mouse_pos):
                            with open('game_saved.txt', "r") as file:
                                mode = str(file.readlines()[3].strip('\n'))
                            Screen.mode_play(self, mode, True)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if MAIN_PLAY_BUTTON.checkForInput(menu_mouse_pos):
                            Screen.play(self)
                        if MAIN_QUIT_BUTTON.checkForInput(menu_mouse_pos):
                            pygame.quit()
                            sys.exit()
            pygame.display.update()

    # перетворення стрічки значень елементів поля гри на матрицю поля гри
    def __codeToBoard(self, code):
        board = [[0 for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for col in range(9):
                board[row][col] = int(code[0])
                code = code[1:]
        return board

    # функція створення ліста з двох порожніх матриць розміром 9х9
    def __empty_code_list(self):
        board = [[0 for _ in range(9)] for _ in range(9)]
        game_matrix = []
        for row in range(2):
            game_matrix.append(board)
        return game_matrix
