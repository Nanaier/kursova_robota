from screen import *

if __name__ == "__main__":
    pygame.init()
    SCREEN = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Sudoku")
    menu = Screen(SCREEN)
    menu.main_menu()
