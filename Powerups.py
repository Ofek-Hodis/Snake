import pygame  # Importing pygame for the creation of the game
import random  # Importing random to generate powerup coordinates
from classes import cell_size, cell_number, screen
from pygame.math import Vector2  # Importing the specific function to facilitate code writing


class SpeedChange:  # Defining a class for the fruits that make the snake grow
    def __init__(self, type, img):
        # Setting up variables with x,y coordinates and the position
        self.x = 0
        self.y = 0  # Defining random y position
        self.position = Vector2(self.x, self.y)
        self.randomize()  # Randomizing the position of the apple
        self.type = type
        self.img = img

    def draw_powerup(self):  # Method to draw the powerup
        powerup_rect = pygame.Rect(int(self.position.x * cell_size), int(self.position.y) * cell_size, cell_size,
                                  cell_size)
        screen.blit(self.img, powerup_rect)  # Placing the image where the rectangle is

    def randomize(self):  # When apple is eaten we will randomize new coordinates for another apple
        self.x = random.randint(0, cell_number - 1)  # Defining random x position on the simulated grid
        self.y = random.randint(0, cell_number - 1)  # Defining random y position
        self.position = Vector2(self.x, self.y)