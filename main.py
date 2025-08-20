import pygame  # Importing pygame for the creation of the game
import sys  # Importing sys to use the exit function to halt the code
from pygame.math import Vector2  # Importing the specific function to facilitate code writing
from button import Button

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

gameover_sound_played = False  # Defining a variable to prevent replay of gameover sound


def gameover_actions():
    global gameover_sound_played  # Letting the function know I use the variable from outside of it
    if not gameover_sound_played:
        # Playing game over sound
        losing_sound = pygame.mixer.Sound('Sounds/game_over.wav')
        losing_sound.set_volume(0.25)  # Lowering the volume of the sound
        losing_sound.play()  # Playing the game over sound
        gameover_sound_played = True


def gamedone_loop():
    main_game = Main()
    while True:
        # Defining a screen of game over
        # gameover_rect = pygame.Rect(0, 0, cell_size * cell_number, cell_size * cell_number)
        # pygame.draw.rect(screen, (20, 20, 20), gameover_rect)
        # Text: Game over. Score: Best score: Replay: Exit:
        screen.fill((20, 20, 20))

        # Setting up restart button
        restart_position = (cell_number/2 * cell_size), (cell_number/2 * cell_size)  # Positioning button
        # Defining font and size
        restart_font = pygame.font.Font('Fonts/Cute Dino.ttf', 35)
        # Using the Button class to create the button
        restart_button = Button(None, restart_position, "Restart", restart_font, (100,100,100), (150,150,150))
        restart_button.update(screen) # The function to display the button
        restart_button.change_color(pygame.mouse.get_pos())  # Checking if the mouse is hovering over the button

        gameover_actions()
        for event in pygame.event.get():  # When starting the game we check for all events
            if event.type == pygame.QUIT:  # If the user closes the window, quit the program
                main_game.close_game()  # Closing game
            if event.type == pygame.KEYDOWN:  # Checking for user input and defining direction by the key
                if event.key == pygame.K_r:
                    global gameover_sound_played  # Telling the function to use the global variable
                    gameover_sound_played = False  # Resetting the variable so the sound will play
                    main_game = Main()  # Restarting the game if the input is r
                    snake_loop()
                elif event.key == pygame.K_ESCAPE:
                    main_game.close_game()  # Closing game

        pygame.display.update()


def snake_loop():
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
            gamedone_loop()
            break

        pygame.display.update()
        clock.tick(60)  # Limiting the loop (and the game) to 60 fps

snake_loop()


