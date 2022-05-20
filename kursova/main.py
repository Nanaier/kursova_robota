from board import *
from button import *
from grid import *
import os
vector = pygame.math.Vector2

class Screen:
    def __init__(self, SCREEN):
        self.SCREEN = SCREEN
        self.running = True
        self.selected = None
        self.hint_cells = []
        self.notCompletedCells = []
        self.x = 410
        self.y = 100
        self.hint_amn = 0

    @staticmethod
    def get_font(size):
        return pygame.font.Font("assets/font.ttf", size)

    def print_text(self, text, pos, size, color=GOLDEN):
        TEXT = Screen.get_font(int(size)).render(text, True, color)
        RECT = TEXT.get_rect(center=pos)
        self.SCREEN.blit(TEXT, RECT)

    def solve_button(self, mode, code):
        self.grid = Grid(self.SCREEN, code, self.x, self.y+40)
        while True:
            PLAY_MOUSE_POS = pygame.mouse.get_pos()
            PLAY_BACK = Button(pos=(640, 670),
                               text_input="BACK", font=Screen.get_font(50), base_color=BLUISH, hovering_color=GOLDEN)
            PLAY_BACK.changeColor(PLAY_MOUSE_POS)
            self.SCREEN.fill(BEIGE)
            PLAY_BACK.update(self.SCREEN)
            self.grid.shadeCells(self.SCREEN)
            self.grid.colorCells(self.SCREEN, "#65C793", self.grid.solvedCells)
            self.grid.drawNumbers(self.SCREEN, code[3])
            self.grid.draw_grid()
            self.print_text("Solved sudoku:", (640, 60), 50)
            self.print_text(mode, (440, 130), 10)
            self.print_text(str(self.hint_amn) + "/3", (840, 130), 10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                        Screen.main_menu(self)

            pygame.display.update()

    def finish_display(self, mode, code):
        self.grid = Grid(self.SCREEN, code, self.x + 300, self.y + 30)
        while True:

            self.SCREEN.fill(BEIGE)

            PLAY_MOUSE_POS = pygame.mouse.get_pos()
            PLAY_BACK = Button(pos=(350, 550),
                               text_input="QUIT", font=Screen.get_font(50), base_color=BLUISH, hovering_color=GOLDEN)
            PLAY_BACK.changeColor(PLAY_MOUSE_POS)
            PLAY_BACK.update(self.SCREEN)
            self.grid.shadeCells(self.SCREEN)

            self.grid.drawNumbers(self.SCREEN, code[3])
            self.grid.draw_grid()
            if code[2] == code[3]:
                self.print_text("You've won!", (640, 60), 50)
                self.print_text("Congratulations!", (340, 250), 35)
                self.print_text("You used " + str(self.hint_amn) + "/3 hints", (340, 400), 35)
                self.print_text(mode, (730, 120), 10)

            else:
                self.print_text("You've lost(", (640, 60), 50)
                self.print_text(mode, (730, 120), 10)
                self.print_text(str(self.hint_amn) + "/3", (1140, 120), 10)
                self.print_text("This was the right", (340, 250), 35)
                self.print_text("sudoku grid:", (340, 400), 35)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                        Screen.main_menu(self)
            pygame.display.update()
    def codeToBoard(self, code):
        board = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        for row in range(9):
            for col in range(9):
                board[row][col] = int(code[0])
                code = code[1:]
        return board
    def empty_code_list(self):
        board = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        code = []
        for row in range(4):
            code.append(board)
        return code

    def mode_play(self, mode, bool):
        if bool == False:
            Brd = Board()
            code = Brd.generateQuestionBoardCode(mode)
            self.grid = Grid(self.SCREEN, code, self.x, self.y)
        else:
            code = self.empty_code_list()
            with open("input.txt", "r") as file:
                l = file.readlines()
                code[2] = self.codeToBoard(l[0])
                code[3] = self.codeToBoard(l[1])

            with open("output.txt", "r") as file:

                l = file.readlines()

                cd = self.codeToBoard(l[0])
                self.hint_amn = int(l[2])
                # self.grid.hint_amount = l[2]
            self.grid = Grid(self.SCREEN, code, self.x, self.y, self.hint_amn)
            code[2] = cd

        self.hint_cells = []
        self.notCompletedCells = []
        while True:
            play_mouse_pos = pygame.mouse.get_pos()
            PLAY_BACK = Button(pos=(640, 670),
                               text_input="BACK", font=Screen.get_font(50), base_color=BLUISH, hovering_color=GOLDEN)
            PLAY_BACK.changeColor(play_mouse_pos)
            self.SCREEN.fill(BEIGE)
            PLAY_BACK.update(self.SCREEN)
            self.grid.shadeCells(self.SCREEN)
            self.grid.colorCells(SCREEN, '#FF6666', self.notCompletedCells)
            self.grid.hint(SCREEN, self.hint_cells)
            if self.selected:
                self.grid.highlightCells(self.SCREEN, self.selected, SHADE)

            self.grid.drawNumbers(self.SCREEN, code[2])


            pygame.draw.rect(self.SCREEN, BLUISH, pygame.Rect(90, 150, 240, 100))
            SOLVE_BUTTON = Button(pos=(210, 200),
                                 text_input="SOLVE", font=Screen.get_font(45), base_color=BEIGE, hovering_color="White")
            pygame.draw.rect(self.SCREEN, BLUISH, pygame.Rect(90, 350, 240, 100))
            HINT_BUTTON = Button(pos=(210, 400),
                                 text_input="HINT", font=Screen.get_font(45), base_color=BEIGE, hovering_color="White")
            pygame.draw.rect(self.SCREEN, BLUISH, pygame.Rect(930, 150, 240, 100))
            CHECK_BUTTON = Button(pos=(1050, 200),
                                 text_input="CHECK", font=Screen.get_font(45), base_color=BEIGE, hovering_color="White")
            pygame.draw.rect(self.SCREEN, BLUISH, pygame.Rect(930, 350, 240, 100))
            SAVE_AND_QUIT_BUTTON = Button(pos=(1050, 400),
                                 text_input="SAVE", font=Screen.get_font(45), base_color=BEIGE, hovering_color="White")

            for button in [SOLVE_BUTTON, HINT_BUTTON, CHECK_BUTTON, SAVE_AND_QUIT_BUTTON]:
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
                        with open("output.txt", "w") as file:
                            file.truncate()
                        Screen.solve_button(self, mode, code)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    selected = self.grid.isOnTheGrid(play_mouse_pos)
                    if selected:
                        self.selected = selected
                    else:
                        self.selected = None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if HINT_BUTTON.checkForInput(play_mouse_pos) and self.grid.hint_amount<3:
                        self.hint_cells.append(self.grid.solve(code[2]))
                        self.hint_amn = self.grid.hint_amount

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if CHECK_BUTTON.checkForInput(play_mouse_pos):
                        if len(self.grid.notComplettedCells(code[2])) != 0:
                            self.notCompletedCells = self.grid.notComplettedCells(code[2])

                        else:
                            with open("output.txt", "w") as file:
                                file.truncate()
                            Screen.finish_display(self, mode, code)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if SAVE_AND_QUIT_BUTTON.checkForInput(play_mouse_pos):
                        with open("output.txt", "w") as file:
                            file.write(self.grid.boardToCode(code[2]) + '\n' + mode + '\n' + str(self.hint_amn))
                if event.type == pygame.KEYDOWN:
                    if self.selected != None and self.selected not in self.grid.lockedCells:
                        if self.isInteger(event.unicode):

                            code[2][self.selected[1]][self.selected[0]] = int(event.unicode)

            self.grid.draw_grid()
            self.print_text(mode, (440, 90), 10)
            self.print_text(str(self.hint_amn) + "/3", (840, 90), 10)
            pygame.display.update()

    def isInteger(self, str):
        try:
            int(str)
            return True
        except:
            return False

    def play(self):
        while True:
            play_mouse_pos = pygame.mouse.get_pos()
            self.SCREEN.fill(BEIGE)
            self.print_text("SELECT YOUR MODE", (640, 60), 60)
            PLAY_BACK = Button(pos=(640, 670),
                               text_input="BACK", font=Screen.get_font(50), base_color=BLUISH, hovering_color=GOLDEN)
            PLAY_BACK.changeColor(play_mouse_pos)
            PLAY_BACK.update(self.SCREEN)
            PLAY_EASY = Button(pos=(640, 200),
                               text_input="EASY MODE", font=Screen.get_font(65), base_color=BLUISH,
                               hovering_color=GOLDEN)
            PLAY_EASY.changeColor(play_mouse_pos)
            PLAY_EASY.update(self.SCREEN)
            PLAY_MEDIUM = Button(pos=(640, 350),
                                 text_input="MEDIUM MODE", font=Screen.get_font(65), base_color=BLUISH,
                                 hovering_color=GOLDEN)
            PLAY_MEDIUM.changeColor(play_mouse_pos)
            PLAY_MEDIUM.update(self.SCREEN)
            PLAY_HARD = Button(pos=(640, 500),
                               text_input="HARD MODE", font=Screen.get_font(65), base_color=BLUISH,
                               hovering_color=GOLDEN)
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

    def main_menu(self):

        while self.running:
            self.SCREEN.fill(BEIGE)
            menu_mouse_pos = pygame.mouse.get_pos()
            self.print_text("SUDOKU", (640, 160), 150)
            if os.stat("output.txt").st_size == 0:
                pygame.draw.rect(self.SCREEN, BLUISH, pygame.Rect(370, 310, 520, 170))
                pygame.draw.rect(self.SCREEN, BLUISH, pygame.Rect(460, 500, 350, 100))
                PLAY_BUTTON = Button(pos=(640, 400),
                                     text_input="PLAY", font=Screen.get_font(120), base_color=BEIGE, hovering_color="White")
                QUIT_BUTTON = Button(pos=(640, 550),
                                     text_input="QUIT", font=Screen.get_font(75), base_color=BEIGE, hovering_color="White")
                for button in [PLAY_BUTTON, QUIT_BUTTON]:
                    button.changeColor(menu_mouse_pos)
                    button.update(self.SCREEN)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if PLAY_BUTTON.checkForInput(menu_mouse_pos):
                            Screen.play(self)
                        if QUIT_BUTTON.checkForInput(menu_mouse_pos):
                            pygame.quit()
                            sys.exit()
            else:
                pygame.draw.rect(self.SCREEN, BLUISH, pygame.Rect(370, 260, 520, 170))
                pygame.draw.rect(self.SCREEN, BLUISH, pygame.Rect(460, 600, 350, 100))
                pygame.draw.rect(self.SCREEN, BLUISH, pygame.Rect(380, 460, 500, 110))
                PLAY_BUTTON = Button(pos=(640, 350),
                                     text_input="PLAY", font=Screen.get_font(120), base_color=BEIGE, hovering_color="White")
                RESUME_BUTTON = Button(pos=(640, 520),
                                     text_input="RESUME", font=Screen.get_font(80), base_color=BEIGE, hovering_color="White")
                QUIT_BUTTON = Button(pos=(640, 650),
                                     text_input="QUIT", font=Screen.get_font(75), base_color=BEIGE, hovering_color="White")
                for button in [PLAY_BUTTON, RESUME_BUTTON, QUIT_BUTTON]:
                    button.changeColor(menu_mouse_pos)
                    button.update(self.SCREEN)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if RESUME_BUTTON.checkForInput(menu_mouse_pos):
                             with open('output.txt', "r") as file:
                                l = file.readlines()
                                lst = []
                                for i in range(len(l)):
                                    lst.append(l[i].strip('\n'))
                                mode = str(lst[1])
                             Screen.mode_play(self, mode, True)

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if PLAY_BUTTON.checkForInput(menu_mouse_pos):
                            Screen.play(self)
                        if QUIT_BUTTON.checkForInput(menu_mouse_pos):
                            pygame.quit()
                            sys.exit()
            pygame.display.update()


if __name__ == "__main__":

    pygame.init()
    SCREEN = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Sudoku")
    menu = Screen(SCREEN)
    menu.main_menu()
