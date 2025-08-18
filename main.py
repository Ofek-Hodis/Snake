import pygame  # Importing pygame for the creation of the game
import sys  # Importing sys to use the exit function to halt the code
from pygame.math import Vector2  # Importing the specific function to facilitate code writing

# Code to set up delay in sound so that it fits the actions
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()  # Initiating pygame

# To import Main we must initiate pygame firstly
from classes import cell_number, cell_size, Main  # Imported variables and the Main class to run the main code

# Creating the window and defining the width and height
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()  # Creating a clock object to define the speed of the game
SCREEN_UPDATE = pygame.USEREVENT  # Creating an event
# Game speed controls:
pygame.time.set_timer(SCREEN_UPDATE, 90)  # Setting a timer to trigger the event every 150 milliseconds

gameover_sound_played = False

main_game = Main()  # An object that will be used to follow the game and execute commands


def gameover_actions():
    global gameover_sound_played  # Letting the function know I use the variable from outside of it
    if not gameover_sound_played:
        # Playing game over sound
        losing_sound = pygame.mixer.Sound('Sounds/game_over.wav')
        losing_sound.set_volume(0.25)  # Lowering the volume of the sound
        losing_sound.play()  # Playing the game over sound
        gameover_sound_played = True

    # Defining a screen of game over
    gameover_rect = pygame.Rect(0, 0, cell_size * cell_number, cell_size * cell_number)
    pygame.draw.rect(screen, (20, 20, 20), gameover_rect)

    # over_text = "Game Over"  # Taking the score based on length acquired (length starts at 3)


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
                    main_game.snake.next_direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:  # Preventing direction change from down to up
                    main_game.snake.next_direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.next_direction = Vector2(1, 0)  # Preventing direction change from left to right
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.next_direction = Vector2(-1, 0)  # Preventing direction change from right to left

            if event.key == pygame.K_r:
                main_game = Main()  # Restarting the game if the input is r
            elif event.key == pygame.K_ESCAPE:
                main_game.close_game()

    screen.fill((175, 215, 70))  # Creating a tuple with rgb values (out of 255) to define the color of the screen
    main_game.draw_elements()
    if not main_game.game_active:  # Updating the screen
        gameover_actions()

    pygame.display.update()
    clock.tick(60)  # Limiting the loop (and the game) to 60 fps


