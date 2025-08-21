import pygame  # Importing pygame for the creation of the game
import sys  # Importing sys to use the exit function to halt the code
from pygame.math import Vector2  # Importing the specific function to facilitate code writing
from button import Button

pygame.init()  # Initiating pygame

# To import Main we must initiate pygame firstly
from classes import cell_number, cell_size, Main  # Imported variables and the Main class to run the main code


# Creating the window and defining the width and height
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()  # Creating a clock object to define the speed of the game
SCREEN_UPDATE = pygame.USEREVENT  # Creating an event
# Game speed controls:
pygame.time.set_timer(SCREEN_UPDATE, 90)  # Setting a timer to trigger the event every 150 milliseconds


def menu_loop():
    while True:
        screen.fill((144, 238, 144))
        title_position = (cell_number / 2 * cell_size), (cell_number / 8 * cell_size)  # Defining position for the text
        title_font = pygame.font.Font('Fonts/Cute Dino.ttf', 50)  # Choice of font
        title_text = title_font.render('Snake', True, (255, 255, 255))
        title_rect = title_text.get_rect(center=title_position)
        screen.blit(title_text, title_rect)


