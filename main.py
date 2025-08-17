import pygame  # Importing pygame for the creation of the game
import sys  # Importing sys to use the exit function to halt the code
import random  # Importing random to generate apple coordinates
from pygame.math import Vector2  # Importing the specific function to facilitate code writing

cell_size = 40  # Defining cell size of cubes in grid (not an actual grid, but will function as one)
cell_number = 20  # Defining the amount of cells in the simulated grid


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]  # Defining the starting position of the snake
        self.direction = Vector2(1, 0)
        self.new_block = False  # Defining a variable to see if we want to add a block to the snake

        self.head_up = pygame.image.load('Images/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Images/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Images/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Images/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Images/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Images/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Images/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Images/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Images/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Images/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Images/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Images/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Images/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Images/body_bl.png').convert_alpha()

    def draw_snake(self):  # Defining method to draw the snake
        self.update_head_graphics()  # Updating the graphics of the head
        self.update_tail_graphics()  # Updating the graphics of the tail

        # Using enumerate to know the index of the block. This way we can check adjacent blocks, necessary for animation
        for index, block in enumerate(self.body):
            x_position = int(block.x * cell_size)  # Calculating the x position
            y_position = int(block.y * cell_size)  # Calculating the y position
            block_rect = pygame.Rect(x_position, y_position, cell_size, cell_size)

            if index == 0:  # Checking if the block is the head of the snake
                screen.blit(self.head, block_rect)
            # Subtract 1 because len is 0 based
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                # Calculating the direction of the next and the previous blocks
                previous_block_direction = self.body[index + 1] - block
                next_block_direction = self.body[index - 1] - block
                # If both blocks have the same x coordinate, the block between them will be vertical
                if previous_block_direction.x == next_block_direction.x:
                    screen.blit(self.body_vertical, block_rect)
                # If both blocks have the same y coordinate, the block between them will be horizontal
                elif previous_block_direction.y == next_block_direction.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if (previous_block_direction.x == -1 and next_block_direction.y == -1 or
                            previous_block_direction.y == -1 and next_block_direction.x == -1):
                        screen.blit(self.body_tl, block_rect)

    def update_head_graphics(self):

        # Based on the direction of the snake, choosing the relevant head image
        if self.direction == Vector2(1, 0):
            self.head = self.head_right
        elif self.direction == Vector2(-1, 0):
            self.head = self.head_left
        elif self.direction == Vector2(0, 1):
            self.head = self.head_down
        elif self.direction == Vector2(0, -1):
            self.head = self.head_up

    def update_tail_graphics(self):
        # Calculating the direction of the tail using the two last blocks
        tail_relation = self.body[len(self.body) - 1] - self.body[len(self.body) - 2]
        # Based on the result, choosing the relevant image
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_down
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_up

    def move_snake(self):  # Method to make the snake move
        if self.new_block:
            body_copy = self.body[:]  # Copying the snakes body
            body_copy.insert(0, body_copy[0] + self.direction)  # Adding a block while moving
            self.body = body_copy
            self.new_block = False  # Resetting the variable to 'False' to avoid an infinitely growing snake
        else:
            body_copy = self.body[:-1]  # Copying items in body from the first to one before the last
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy

    def add_block(self):
        self.new_block = True  # Changing this variable to make the snake linger when running move_snake()


class Fruit:  # Defining a class for the fruits that make the snake grow
    def __init__(self):
        # Setting up variables with x,y coordinates and the position
        self.x = 0
        self.y = 0  # Defining random y position
        self.position = Vector2(self.x, self.y)
        self.randomize()  # Randomizing the position of the apple

    def draw_fruit(self):  # Method to draw the fruit
        # Creating a rectangle with given positions, width and height
        fruit_rect = pygame.Rect(int(self.position.x * cell_size), int(self.position.y) * cell_size, cell_size,
                                 cell_size)
        screen.blit(apple, fruit_rect)  # Placing the image where the rectangle is
        # Drawing a rectangle on screen, with an rgb tuple for colors, using the previously created rect
        # pygame.draw.rect(screen, (200, 40, 10), fruit_rect)

    def randomize(self):  # When apple is eaten we will randomize new coordinates for another apple
        self.x = random.randint(0, cell_number - 1)  # Defining random x position on the simulated grid
        self.y = random.randint(0, cell_number - 1)  # Defining random y position
        self.position = Vector2(self.x, self.y)


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):  # Method to move the snake when the game updates
        self.snake.move_snake()  # Moving the snake every update
        self.check_collision()  # Checking for collision with an apple
        self.check_fail()  # Checking if the player lost

    def draw_elements(self):  # Method to draw the fruit and snake
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        if self.fruit.position == self.snake.body[0]:
            self.fruit.randomize()  # Changing location of the fruit
            self.snake.add_block()  # Making the snake longer

    def check_fail(self):  # Checking if the player failed and the game should be over
        # The cell farther right is cell 19 (cells are 0 bsed), we use 'x < cell_number' instead of '<='
        if (not 0 <= self.snake.body[0].x < cell_number) or (not 0 <= self.snake.body[0].y < cell_number):
            self.game_over()  # Quitting the game if the snake is not within the borders

        # Comparing th head's coordinates to the rest of the body (excluding the head)
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()  # Quitting the game if the snake collided with it self

    def game_over(self):  # Method to quit the game
        print("Game over :(")
        pygame.quit()
        sys.exit()


pygame.init()  # Initiating pygame
# Creating the window and defining the width and height
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()  # Creating a clock object to define the speed of the game
# Taking an apple photo and converting it to a format pygame can handle easily
apple = pygame.image.load('Images/apple.png').convert_alpha()
apple = pygame.transform.scale(apple, (cell_size, cell_size))  # Conversion of the photo to size of one cell

SCREEN_UPDATE = pygame.USEREVENT  # Creating an event
# Game speed controls:
pygame.time.set_timer(SCREEN_UPDATE, 150)  # Setting a timer to trigger the event every 150 milli-seconds

main_game = Main()  # An object that will be used to follow the game and execute commands

while True:  # Infinite loop I will break when I want the game to stop
    for event in pygame.event.get():  # When starting the game we check for all events
        if event.type == pygame.QUIT:  # If the user closes the window, quit the program
            pygame.quit()
            sys.exit()  # Halting the code
        if event.type == SCREEN_UPDATE:  # Moving the snake constantly when updating the screen
            main_game.update()
        if event.type == pygame.KEYDOWN:  # Checking for user input and defining direction by the key
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:  # Preventing direction change from up to down
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:  # Preventing direction change from down to up
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)  # Preventing direction change from left to right
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)  # Preventing direction change from right to left

    screen.fill((175, 215, 70))  # Creating a tuple with rgb values (out of 255) to define the color of the screen
    main_game.draw_elements()
    pygame.display.update()  # Updating the screen
    clock.tick(60)  # Limiting the loop (and the game) to 60 fps
