# клас, який відповідає за створення кнопки
class Button:
    def __init__(self, pos, text_input, font, base_color, hovering_color):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    # оновити кнопку на екрані
    def update(self, screen):
        screen.blit(self.text, self.text_rect)

    # перевірити чи курсор мишки над кнопкою
    def checkForInput(self, position):
        if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top,
                                                                                                    self.text_rect.bottom):
            return True
        return False

    # змінити колір кнопки при наведенні на неї
    def changeColor(self, position):
        if self.checkForInput(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
