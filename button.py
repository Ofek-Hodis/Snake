#pygame.transform.scale() to use laaaater

class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        # Defining the self attributes to those received
        self.image = image  # This will also define the size of the button (unless set to none)
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.text_input = text_input
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        # Applying the text input, font and color
        self.text = self.font.render(self.text_input, True, self.base_color)

        if self.image is None:
            self.image = self.text
        # Defining a rectangle for the background of the button
        self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))
        # Defining a rectangle for the text of the button
        self.text_rect = self.text.get_rect(center = (self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:  # Drawing the image if there is one
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_input(self, position):
        # Checking if the given position (x and y coordinates) is within the rect borders
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def change_color(self, position):
        # Checking if the mouse is hovering on the text
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)