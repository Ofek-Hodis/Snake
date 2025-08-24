import pygame  # Importing pygame for the creation of the game
import sys  # Importing sys to use the exit function to halt the code
from pygame.math import Vector2  # Importing the specific function to facilitate code writing
from button import Button

# Code to set up delay in sound so that it fits the actions
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()  # Initiating pygame

# To import Main we must initiate pygame firstly
from classes import cell_number, cell_size, Main  # Imported variables and the Main class to run the main code
from menu_drawing import title_draw

# Creating the window and defining the width and height
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()  # Creating a clock object to define the speed of the game
SCREEN_UPDATE = pygame.USEREVENT  # Creating an event
# Game speed controls:
pygame.time.set_timer(SCREEN_UPDATE, 90)  # Setting a timer to trigger the event every 150 milliseconds

gameover_sound_played = False  # Defining a variable to prevent replay of gameover sound
font = 'Fonts/Cute Dino.ttf'


def menu_loop():
    global font  # Telling the function to use the global font variable
    while True:
        screen.fill((175, 215, 70))

        title_position = (cell_number / 2 * cell_size), (3 * cell_size)  # Defining position for the text
        # Using a function to draw the title
        title_draw("snake", title_position, font, 50, (255, 255, 255), screen)

        # Setting up start (singleplayer) button
        start_position = (cell_number / 2 * cell_size), (10 * cell_size)  # Positioning button
        # Defining font and size
        start_font = pygame.font.Font(font, 35)
        # Using the Button class to create the button
        start_button = Button(None, start_position, "Single player mode", start_font, (100, 100, 100), (150, 150, 150))
        start_button.update(screen)  # The function to display the button
        start_button.change_color(pygame.mouse.get_pos())  # Checking if the mouse is hovering over the button
        screen.blit(start_button.text, start_button.rect)

        # Setting up two player start button
        two_player_position = (cell_number / 2 * cell_size), (12 * cell_size)  # Positioning button
        # Defining font and size
        two_player_font = pygame.font.Font(font, 35)
        # Using the Button class to create the button
        two_player_button = Button(None, two_player_position, "Two player mode", start_font, (100, 100, 100), (150, 150, 150))
        two_player_button.update(screen)  # The function to display the button
        two_player_button.change_color(pygame.mouse.get_pos())  # Checking if the mouse is hovering over the button
        screen.blit(two_player_button.text, two_player_button.rect)

        # Setting up quit button
        quit_position = (cell_number / 2 * cell_size), (14 * cell_size)  # Positioning button
        # Defining font and size
        quit_font = pygame.font.Font(font, 35)
        # Using the Button class to create the button
        quit_button = Button(None, quit_position, "Quit", quit_font, (100, 100, 100), (150, 150, 150))
        quit_button.update(screen)  # The function to display the button
        quit_button.change_color(pygame.mouse.get_pos())  # Checking if the mouse is hovering over the button
        screen.blit(quit_button.text, quit_button.rect)

        for event in pygame.event.get():  # When starting the game we check for all events
            if event.type == pygame.QUIT:  # If the user closes the window, quit the program
                pygame.quit()  # Closing game
                sys.exit()
            if event.type == pygame.KEYDOWN:  # Checking for user input and defining direction by the key
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()  # Closing game
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Checking if the player pressed a button
                if start_button.check_input(pygame.mouse.get_pos()):
                    snake_loop()
                    break
                elif two_player_button.check_input(pygame.mouse.get_pos()):
                    twoplayer_loop()
                    break
                elif quit_button.check_input(pygame.mouse.get_pos()):
                    pygame.quit()  # Closing game
                    sys.exit()

        pygame.display.update()


def gameover_actions():
    global gameover_sound_played  # Letting the function know I use the variable from outside of it
    if not gameover_sound_played:
        # Playing game over sound
        losing_sound = pygame.mixer.Sound('Sounds/game_over.wav')
        losing_sound.set_volume(0.25)  # Lowering the volume of the sound
        losing_sound.play()  # Playing the game over sound
        gameover_sound_played = True


def gamedone_loop(score):
    main_game = Main()
    global gameover_sound_played  # Telling the function to use the global variable
    global font

    while True:#Score and best score
        screen.fill((20, 20, 20))

        title_position = (cell_number/2 * cell_size), (3 * cell_size)  # Defining position for the text
        # Using a function to draw the title
        title_draw("Game Over", title_position, font, 50, (255, 255, 255), screen)

        score_position = (cell_number / 2 * cell_size), (5 * cell_size)  # Defining position for the text
        # Using a function to draw the score
        title_draw("Final Score: " + str(score), score_position, font, 35, (255, 255, 255), screen)

        # Setting up restart button
        restart_position = (cell_number/2 * cell_size), (10 * cell_size)  # Positioning button
        # Defining font and size
        restart_font = pygame.font.Font(font, 35)
        # Using the Button class to create the button
        restart_button = Button(None, restart_position, "Restart", restart_font, (100,100,100), (150,150,150))
        restart_button.update(screen) # The function to display the button
        restart_button.change_color(pygame.mouse.get_pos())  # Checking if the mouse is hovering over the button
        screen.blit(restart_button.text, restart_button.rect)

        # Setting up quit button
        quit_position = (cell_number / 2 * cell_size), (12 * cell_size)  # Positioning button
        # Defining font and size
        quit_font = pygame.font.Font(font, 35)
        # Using the Button class to create the button
        quit_button = Button(None, quit_position, "Quit", quit_font, (100, 100, 100), (150, 150, 150))
        quit_button.update(screen)  # The function to display the button
        quit_button.change_color(pygame.mouse.get_pos())  # Checking if the mouse is hovering over the button
        screen.blit(quit_button.text, quit_button.rect)

        gameover_actions()
        for event in pygame.event.get():  # When starting the game we check for all events
            if event.type == pygame.QUIT:  # If the user closes the window, quit the program
                main_game.close_game()  # Closing game
            if event.type == pygame.KEYDOWN:  # Checking for user input and defining direction by the key
                if event.key == pygame.K_r:
                    gameover_sound_played = False  # Resetting the variable so the sound will play
                    main_game = Main()  # Restarting the game if the input is r
                    snake_loop()
                elif event.key == pygame.K_ESCAPE:
                    main_game.close_game()  # Closing game
            if event.type == pygame.MOUSEBUTTONDOWN:  # Checking if the player pressed a button
                if restart_button.check_input(pygame.mouse.get_pos()):
                    gameover_sound_played = False  # Resetting the variable so the sound will play
                    main_game = Main()  # Restarting the game if the input is r
                    snake_loop()
                elif quit_button.check_input(pygame.mouse.get_pos()):  # Quitting if button was pressed
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
            gamedone_loop(len(main_game.snake.body) - 3)  # Calculating the final score
            break

        pygame.display.update()
        clock.tick(60)  # Limiting the loop (and the game) to 60 fps


def twoplayer_loop():
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
            gamedone_loop(len(main_game.snake.body) - 3)  # Calculating the final score
            break

        pygame.display.update()
        clock.tick(60)  # Limiting the loop (and the game) to 60 fps


menu_loop()


