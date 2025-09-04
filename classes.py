import pygame  # Importing pygame for the creation of the game
import sys  # Importing sys to use the exit function to halt the code
import random  # Importing random to generate fruit coordinates
from pygame.math import Vector2  # Importing the specific function to facilitate code writing
from datetime import datetime  # Imported for debugging purposes

cell_size = 30  # Defining cell size of cubes in grid (not an actual grid, but will function as one)
cell_number = 25  # Defining the amount of cells in the simulated grid
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))

game_font = pygame.font.Font('Fonts/Cute Dino.ttf', 25)  # Choosing the font for the score


class Snake:
    def __init__(self, position=(5, 4, 3), height=5, direction=1, snake_number=1):
        # Defining the starting position of the snake
        self.body = [Vector2(position[0], height), Vector2(position[1], height), Vector2(position[2], height)]
        self.direction = Vector2(direction, 0)
        self.next_direction = self.direction
        self.new_block = False  # Defining a variable to see if we want to add a block to the snake
        self.number = snake_number

        # Choosing image folder fitting to snake number
        if self.number == 1:
            snake_folder = 'snake1'
        elif self.number == 2:
            snake_folder = 'snake2'

        # Using f string to format the folder name
        # Defining head locations to relevant photos and adjusting the size to that of one cell
        self.head_up = pygame.image.load(f'Images/{snake_folder}/head_up.png').convert_alpha()
        self.head_up = pygame.transform.scale(self.head_up, (cell_size, cell_size))
        self.head_down = pygame.image.load(f'Images/{snake_folder}/head_down.png').convert_alpha()
        self.head_down = pygame.transform.scale(self.head_down, (cell_size, cell_size))
        self.head_right = pygame.image.load(f'Images/{snake_folder}/head_right.png').convert_alpha()
        self.head_right = pygame.transform.scale(self.head_right, (cell_size, cell_size))
        self.head_left = pygame.image.load(f'Images/{snake_folder}/head_left.png').convert_alpha()
        self.head_left = pygame.transform.scale(self.head_left, (cell_size, cell_size))

        # Defining tail locations to relevant photos and adjusting the size to that of one cell
        self.tail_up = pygame.image.load(f'Images/{snake_folder}/tail_up.png').convert_alpha()
        self.tail_up = pygame.transform.scale(self.tail_up, (cell_size, cell_size))
        self.tail_down = pygame.image.load(f'Images/{snake_folder}/tail_down.png').convert_alpha()
        self.tail_down = pygame.transform.scale(self.tail_down, (cell_size, cell_size))
        self.tail_right = pygame.image.load(f'Images/{snake_folder}/tail_right.png').convert_alpha()
        self.tail_right = pygame.transform.scale(self.tail_right, (cell_size, cell_size))
        self.tail_left = pygame.image.load(f'Images/{snake_folder}/tail_left.png').convert_alpha()
        self.tail_left = pygame.transform.scale(self.tail_left, (cell_size, cell_size))

        # Defining body locations to relevant photos and adjusting the size to that of one cell
        self.body_vertical = pygame.image.load(f'Images/{snake_folder}/body_vertical.png').convert_alpha()
        self.body_vertical = pygame.transform.scale(self.body_vertical, (cell_size, cell_size))
        self.body_horizontal = pygame.image.load(f'Images/{snake_folder}/body_horizontal.png').convert_alpha()
        self.body_horizontal = pygame.transform.scale(self.body_horizontal, (cell_size, cell_size))

        # Defining curved bodyparts locations to relevant photos and adjusting the size to that of one cell
        self.body_tr = pygame.image.load(f'Images/{snake_folder}/body_tr.png').convert_alpha()
        self.body_tr = pygame.transform.scale(self.body_tr, (cell_size, cell_size))
        self.body_tl = pygame.image.load(f'Images/{snake_folder}/body_tl.png').convert_alpha()
        self.body_tl = pygame.transform.scale(self.body_tl, (cell_size, cell_size))
        self.body_br = pygame.image.load(f'Images/{snake_folder}/body_br.png').convert_alpha()
        self.body_br = pygame.transform.scale(self.body_br, (cell_size, cell_size))
        self.body_bl = pygame.image.load(f'Images/{snake_folder}/body_bl.png').convert_alpha()
        self.body_bl = pygame.transform.scale(self.body_bl, (cell_size, cell_size))

        self.eat_sound = pygame.mixer.Sound('Sounds/apple_eaten.wav')  # Adding apple sound
        self.eat_sound.set_volume(0.25)  # Lowering the volume of the sound

    def play_eat_sound(self):
        self.eat_sound.play()

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
                    # If there's one block to the left and one on top of the current block, we choose the fitting
                    # animation (the direction of the smale itself doesn't matter)
                    # Calculations done each time to determine filling animation
                    if (previous_block_direction.x == -1 and next_block_direction.y == -1 or
                            previous_block_direction.y == -1 and next_block_direction.x == -1):
                        screen.blit(self.body_tl, block_rect)
                    elif (previous_block_direction.x == 1 and next_block_direction.y == 1 or
                            previous_block_direction.y == 1 and next_block_direction.x == 1):
                        screen.blit(self.body_br, block_rect)
                    elif (previous_block_direction.x == 1 and next_block_direction.y == -1 or
                            previous_block_direction.y == -1 and next_block_direction.x == 1):
                        screen.blit(self.body_tr, block_rect)
                    elif (previous_block_direction.x == -1 and next_block_direction.y == 1 or
                            previous_block_direction.y == 1 and next_block_direction.x == -1):
                        screen.blit(self.body_bl, block_rect)

    def update_head_graphics(self): # # Based on the direction of the snake, choosing the relevant head image
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
        # Only change direction if it's not the reverse of current direction
        if (self.next_direction + self.direction) != Vector2(0, 0):
            self.direction = self.next_direction

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
        self.new_block = True  # Changing this variable to make the snake longer when running move_snake()


class Fruit:  # Defining a class for the fruits that make the snake grow
    def __init__(self, img='Images/apple.png'):
        # Setting up variables with x,y coordinates and the position
        self.x = 0
        self.y = 0  # Defining random y position
        self.image = pygame.image.load(img).convert_alpha()  # Setting up the apple image
        # Conversion of the photo to size of one cell
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
        self.position = Vector2(self.x, self.y)
        self.randomize()  # Randomizing the position of the apple

    def draw_fruit(self):  # Method to draw the fruit
        # Creating a rectangle with given positions, width and height
        fruit_rect = pygame.Rect(int(self.position.x * cell_size), int(self.position.y) * cell_size, cell_size,
                                 cell_size)
        screen.blit(self.image, fruit_rect)  # Placing the image where the rectangle i

    def randomize(self, snake1=Snake(), snake2=Snake(), twoplayers=False):  # When apple is eaten we will randomize new coordinates for another apple
        while True:
            self.x = random.randint(0, cell_number - 1)  # Defining random x position on the simulated grid
            self.y = random.randint(0, cell_number - 1)  # Defining random y position
            self.position = Vector2(self.x, self.y)
            if twoplayers:
                if self.position not in snake1.body and self.position not in snake2.body:
                    break
            elif self.position not in snake1.body:
                break


class Powerup:  # Defining a class for the fruits that make the snake grow
    def __init__(self, img='Images/apple.png'):
        # Setting up variables with x,y coordinates and the position
        self.x = 0
        self.y = 0  # Defining random y position
        self.image = pygame.image.load(img).convert_alpha()  # Setting up the apple image
        # Conversion of the photo to size of one cell
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
        self.position = Vector2(self.x, self.y)
        self.randomize()  # Randomizing the position of the apple
        self.is_powerup = False

    # Method to check if the powerup should be drawed and draw it if so
    def draw_check(self, time):
        # Every 5 seconds of game time (if there is no powerup) giving a 1 in 4 chance to spawn a power up
        if time % 5 == 0 and not self.is_powerup:
            spawn_chance = random.randint(0, 3)
            if spawn_chance == 0:
                self.draw_powerup()
                return True
        return False

    def draw_powerup(self):  # Method to draw the powerup
        powerup_rect = pygame.Rect(int(self.position.x * cell_size), int(self.position.y) * cell_size, cell_size,
                                   cell_size)
        screen.blit(self.image, powerup_rect)  # Placing the image where the rectangle is
        self.is_powerup = True

    def randomize(self, snake1=Snake(), snake2=Snake(),
                  twoplayers=False):  # When apple is eaten we will randomize new coordinates for another apple
        while True:
            self.x = random.randint(0, cell_number - 1)  # Defining random x position on the simulated grid
            self.y = random.randint(0, cell_number - 1)  # Defining random y position
            self.position = Vector2(self.x, self.y)
            if twoplayers:
                if self.position not in snake1.body and self.position not in snake2.body:
                    break
            elif self.position not in snake1.body:
                break

    def get_effect(self):
        if self.type == 0:
            return 50
        elif self.type == 1:
            return 200


class Main:
    def __init__(self, twoplayers=False):
        self.snake = Snake()
        self.snake2 = Snake((19, 20, 21), 20, -1, 2)  # Changing position for the second snake
        self.fruit = Fruit()
        self.fruit2 = Fruit('Images/orange.png')  # Different photo for the second fruit
        self.game_active = True  # Controlling game state
        self.two_players = twoplayers  # Storing if the game is in two player mode or not
        self.power_up = Powerup()  # Creating a power up

    def update(self):  # Method to move the snake when the game updates
        if self.game_active:
            self.snake.move_snake()  # Moving the snake every update
            if self.two_players:  # Moving the second snake before checking for collisions to keep the game updated
                self.snake2.move_snake()
            self.check_collision()  # Checking for collision with an apple
            self.check_fail()  # Checking if the player lost
            if self.two_players:
                self.check_fail_two()  # Checking if the second snake fails

    def draw_elements(self):  # Method to draw the fruit, snake and the score
        if self.game_active:
            self.draw_grass()
            self.fruit.draw_fruit()
            self.snake.draw_snake()
            self.draw_score()
        if self.two_players:
            self.snake2.draw_snake()
            self.fruit2.draw_fruit()

    def check_collision(self):
        if self.fruit.position == self.snake.body[0]:
            self.fruit.randomize(self.snake, self.snake2, self.two_players)  # Changing location of the fruit
            self.snake.add_block()  # Making the snake longer
            self.snake.play_eat_sound()  # Playing sound of apple eaten

        if self.two_players:
            if self.fruit2.position == self.snake2.body[0]:
                self.fruit2.randomize(self.snake, self.snake2, self.two_players)  # Changing location of the fruit
                self.snake2.add_block()  # Making the snake longer
                self.snake2.play_eat_sound()  # Playing sound of apple eaten

    def check_fail(self):  # Checking if the player failed and the game should be over
        # The cell number is are 0 based, so we subtract 1
        if (not 0 <= self.snake.body[0].x < cell_number) or (not 0 <= self.snake.body[0].y < cell_number):
            print("Snake out of bounds!")
            self.game_active = False  # Changing to false so the game stops running

        # Comparing th head's coordinates to the rest of the body (excluding the head)
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                print("Snake collided with itself!")
                self.game_active = False  # Changing to false so the game stops running


    def check_fail_two(self):
        # Checking if snake 2 is out of bounds
        if (not 0 <= self.snake2.body[0].x < cell_number) or (not 0 <= self.snake2.body[0].y < cell_number):
            print("Snake 2 out of bounds!")
            self.game_active = False  # Changing to false so the game stops running

        # Checking if snake2 collided with itself
        for block in self.snake2.body[1:]:
            if block == self.snake2.body[0]:
                print("Snake 2 collided with itself!")
                self.game_active = False  # Changing to false so the game stops running

        # Checking if snake1 collided with snake2
        for block in self.snake.body[1:]:
            if block == self.snake2.body[0]:
                print("Snake 2 collided with snake 1!")
                self.game_active = False  # Changing to false so the game stops running

        # Checking if snake2 collided with snake1
        for block in self.snake2.body[1:]:
            if block == self.snake.body[0]:
                print("Snake 1 collided with snake 2!")
                self.game_active = False  # Changing to false so the game stops running


    @staticmethod  # The method doesn't use self
    def close_game():  # Method to quit the game
        pygame.quit()
        sys.exit()

    @staticmethod
    def draw_grass():
        grass_color = (167, 209, 61)
        for row in range(cell_number):  # Going row by row and coloring every other one
            if row % 2 == 0:
                for col in range(cell_number):  # Going column by column and coloring the even grid parts
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):  # Going column by column and coloring the odd grid parts
                    if col % 2 != 0:  # Choosing every other column (odd numbers)
                        grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        if not self.two_players:
            score_text = str(len(self.snake.body) - 3)  # Taking the score based on length acquired (length starts at 3)
        else:
            score_text = str(len(self.snake.body)-3 + len(self.snake2.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 30)  # Defining the coordinates for the score
        score_y = int(cell_size * cell_number - 30)
        # Placing the center of the score rectangle in the coordinates
        score_rect = score_surface.get_rect(center=(score_x, score_y))

        screen.blit(score_surface, score_rect)


