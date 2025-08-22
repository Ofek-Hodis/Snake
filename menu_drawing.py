import pygame  # Importing pygame for the creation of the game
import sys  # Importing sys to use the exit function to halt the code
from pygame.math import Vector2  # Importing the specific function to facilitate code writing
from button import Button

# To import Main we must initiate pygame firstly
from classes import cell_number, cell_size, Main  # Imported variables and the Main class to run the main code


def title_draw(text, position, title_font, size, color, screen):
    font = pygame.font.Font(title_font, size)
    title_text = font.render(text, True, color)
    title_rect = title_text.get_rect(center=position)
    screen.blit(title_text, title_rect)




