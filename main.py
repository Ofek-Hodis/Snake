import pygame  # Importing pygame for the creation of the game
import sys  # Importing sys to use the exit function to halt the code
from pygame.math import Vector2  # Importing the specific function to facilitate code writing
from button import Button  # Importing button class
import random  # Importing random to generate fruit coordinates

# Importing functions to store and get high score
from support_funcs import get_high_score, get_high_score_twoplayer, store_high_score, store_high_score_twoplayer

# Code to set up delay in sound so that it fits the actions
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()  # Initiating pygame

# To import Main we must initiate pygame firstly
from main_classes import cell_number, cell_size, Main  # Imported variables and the Main class to run the main code
from support_funcs import text_draw

# Creating the window and defining the width and height
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()  # Creating a clock object to define the speed of the game
SCREEN_UPDATE = pygame.USEREVENT  # Creating an event
pygame.time.set_timer(SCREEN_UPDATE, 140)  # Setting a timer (milliseconds) to trigger the event (game speed)

gameover_sound_played = False  # Defining a variable to prevent replay of gameover sound
font = 'Fonts/Cute Dino.ttf'


def menu_loop():
    global font  # Telling the function to use the global font variable
    while True:
        screen.fill((175, 215, 70))

        title_position = (cell_number / 2 * cell_size), (3 * cell_size)  # Defining position for the text
        # Using a function to draw the title
        text_draw("snake", title_position, font, 50, (255, 255, 255), screen)

        # Setting up start (singleplayer) button
        start_position = (cell_number / 2 * cell_size), (10 * cell_size)  # Positioning button
        # Defining font and size
        start_font = pygame.font.Font(font, 35)
        # Using the Button class to create the button
        start_button = Button(None, start_position, "Single player mode", start_font,
                              (100, 100, 100), (150, 150, 150), "Sounds/menu_select.wav")
        start_button.update(screen)  # The function to display the button
        start_button.change_color(pygame.mouse.get_pos())  # Checking if the mouse is hovering over the button
        screen.blit(start_button.text, start_button.rect)

        # Setting up two player start button
        two_player_position = (cell_number / 2 * cell_size), (12 * cell_size)  # Positioning button
        # Defining font and size
        two_player_font = pygame.font.Font(font, 35)
        # Using the Button class to create the button
        two_player_button = Button(None, two_player_position, "Two player mode", start_font,
                                   (100, 100, 100), (150, 150, 150), "Sounds/menu_select.wav")
        two_player_button.update(screen)  # The function to display the button
        two_player_button.change_color(pygame.mouse.get_pos())  # Checking if the mouse is hovering over the button
        screen.blit(two_player_button.text, two_player_button.rect)

        # Setting up quit button
        quit_position = (cell_number / 2 * cell_size), (14 * cell_size)  # Positioning button
        # Defining font and size
        quit_font = pygame.font.Font(font, 35)
        # Using the Button class to create the button
        quit_button = Button(None, quit_position, "Quit", quit_font,
                             (100, 100, 100), (150, 150, 150), "Sounds/menu_select.wav")
        quit_button.update(screen)  # The function to display the button
        quit_button.change_color(pygame.mouse.get_pos())  # Checking if the mouse is hovering over the button
        screen.blit(quit_button.text, quit_button.rect)

        for event in pygame.event.get():  # When starting the game we check for all events
            if event.type == pygame.QUIT:  # If the user closes the window, quit the program
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # Checking for user input and defining direction by the key
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            # Checking if the player pressed the mouse button and activating fitting button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.check_input(pygame.mouse.get_pos()):
                    snake_loop()
                    break
                elif two_player_button.check_input(pygame.mouse.get_pos()):
                    twoplayer_loop()
                    break
                elif quit_button.check_input(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def gameover_actions(score, main):
    global gameover_sound_played  # Letting the function know I use the variable from outside of it
    if not gameover_sound_played:
        # Playing game over sound
        losing_sound = pygame.mixer.Sound('Sounds/game_over.wav')
        losing_sound.set_volume(0.15)  # Lowering the volume of the sound
        losing_sound.play()  # Playing the game over sound
        gameover_sound_played = True
    if main.two_players:
        top_score = get_high_score_twoplayer()
    else:
        top_score = get_high_score()
    if score > top_score:  # Returning a message to be displayed based on user's performance
        if main.two_players:
            store_high_score_twoplayer(score)
        else:
            store_high_score(score)
        return "Congratulations! You broke your high score!"
    elif score == top_score:
        return "You almost broke your high score! You didn't tho."
    return ""


def gamedone_loop(score, time, main):
    global gameover_sound_played  # Telling the function to use the global variable
    global font

    score_msg = gameover_actions(score, main)  # Storing if the player broke the high score or not

    while True:
        screen.fill((20, 20, 20))

        title_position = (cell_number / 2 * cell_size), (3 * cell_size)  # Defining position for the text
        # Using a function to draw the title
        text_draw("Game Over", title_position, font, 50, (255, 255, 255), screen)

        score_position = (cell_number / 2 * cell_size), (6 * cell_size)  # Defining position for the text
        # Using a function to draw the score
        text_draw("Final Score: " + str(score), score_position, font, 30, (175, 175, 175), screen)

        high_score_position = (cell_number / 2 * cell_size), (8 * cell_size)  # Defining position for the text
        if main.two_players:
            high_score = get_high_score_twoplayer()
        else:
            high_score = get_high_score()  # Getting high score from JSON file
        # Using a function to draw the high score
        text_draw("High Score: " + str(high_score), high_score_position, font, 30, (175, 175, 175), screen)

        time_position = (cell_number / 2 * cell_size), (10 * cell_size)  # Defining position for the text
        time_text = str(time)
        # Using a function to draw the time
        text_draw("Total time: " + time_text + " Seconds", time_position, font, 30, (175, 175, 175), screen)

        score_msg_position = (cell_number / 2 * cell_size), (12 * cell_size)  # Defining position for the text
        # Using a function to draw the score message
        text_draw(score_msg, score_msg_position, font, 25, (175, 175, 175), screen)

        # Setting up single player button
        single_position = (cell_number / 2 * cell_size), (16 * cell_size)  # Positioning button
        # Defining font and size
        single_font = pygame.font.Font(font, 35)
        # Using the Button class to create the button
        single_button = Button(None, single_position, "Single player mode", single_font,
                                (100, 100, 100), (200, 200, 200), "Sounds/menu_select.wav")
        single_button.update(screen)  # The function to display the button
        single_button.change_color(pygame.mouse.get_pos())  # Checking if the mouse is hovering over the button
        screen.blit(single_button.text, single_button.rect)

        # Setting up two player button
        two_position = (cell_number / 2 * cell_size), (19 * cell_size)  # Positioning button
        # Defining font and size
        two_font = pygame.font.Font(font, 35)
        # Using the Button class to create the button
        two_button = Button(None, two_position, "Two players mode", two_font,
                               (100, 100, 100), (200, 200, 200), "Sounds/menu_select.wav")
        two_button.update(screen)  # The function to display the button
        two_button.change_color(pygame.mouse.get_pos())  # Checking if the mouse is hovering over the button
        screen.blit(two_button.text, two_button.rect)

        # Setting up quit button
        quit_position = (cell_number / 2 * cell_size), (22 * cell_size)  # Positioning button
        # Defining font and size
        quit_font = pygame.font.Font(font, 35)
        # Using the Button class to create the button
        quit_button = Button(None, quit_position, "Quit", quit_font,
                             (100, 100, 100), (200, 200, 200), "Sounds/menu_select.wav")
        quit_button.update(screen)  # The function to display the button
        quit_button.change_color(pygame.mouse.get_pos())  # Checking if the mouse is hovering over the button
        screen.blit(quit_button.text, quit_button.rect)

        for event in pygame.event.get():  # When starting the game we check for all events
            if event.type == pygame.QUIT:  # If the user closes the window, quit the program
                main.close_game()  # Closing game
            if event.type == pygame.KEYDOWN:  # Checking for user input and defining direction by the key
                if event.key == pygame.K_r:
                    gameover_sound_played = False  # Resetting the variable so the sound will play
                    main_game = Main()  # Restarting the game if the input is r
                    snake_loop()
                elif event.key == pygame.K_ESCAPE:
                    main.close_game()  # Closing game
            if event.type == pygame.MOUSEBUTTONDOWN:  # Checking if the player pressed a button
                if single_button.check_input(pygame.mouse.get_pos()):
                    gameover_sound_played = False  # Resetting the variable so the sound will play
                    main = Main()  # Restarting the game if the input is r
                    snake_loop()
                elif two_button.check_input(pygame.mouse.get_pos()):
                    gameover_sound_played = False  # Resetting the variable so the sound will play
                    main = Main()  # Restarting the game if the input is r
                    twoplayer_loop()
                elif quit_button.check_input(pygame.mouse.get_pos()):  # Quitting if button was pressed
                    main.close_game()  # Closing game

        pygame.display.update()


def snake_loop():
    main_game = Main()  # An object that will be used to follow the game and execute commands
    time_start = pygame.time.get_ticks()  # storing time at start to calculate run time
    power_up_start = 5  # Set to 5 to avoid activation before first spawn
    power_up_time = 10
    main_game.power_up.is_eaten = False  # Variable to tell the powerup's effects should be activated
    is_normal_speed = False  # Variable to track if game speed has been changed

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
                        main_game.snake.next_direction = Vector2(-1,
                                                                 0)  # Preventing direction change from right to left

                if event.key == pygame.K_r:
                    main_game = Main()  # Restarting the game if the input is r
                elif event.key == pygame.K_ESCAPE:
                    main_game.close_game()

        screen.fill((175, 215, 70))  # rgb tuple defines color of screen
        # Storing time elapsed to calculate whether powerup should be spawned
        time_elapsed = (pygame.time.get_ticks() - time_start) / 1000
        # Can only spawn powerup after 5 seconds of gameplay and 5 seconds after the previous powerup was taken
        if time_elapsed > 5 and not main_game.power_up.is_drawn and power_up_time >= 10:
            main_game.power_up.draw_check()
        main_game.draw_elements()

        if main_game.power_up.is_eaten:
            print("eaten")
            power_up_start = pygame.time.get_ticks()  # Storing activation time for powerup
            if main_game.power_up.type == 0:  # Powerup effect according to it's type
                pygame.time.set_timer(SCREEN_UPDATE, 90)
                print("speed")
            elif main_game.power_up.type == 1:
                pygame.time.set_timer(SCREEN_UPDATE, 220)
                print("slow")
            main_game.power_up.is_eaten = False
            is_normal_speed = False

        power_up_time = (pygame.time.get_ticks()-power_up_start)/1000
        if power_up_time >= 5 and not is_normal_speed:  # Canceling powerup effect after 5 seconds
            pygame.time.set_timer(SCREEN_UPDATE, 140)
            print("normal")
            is_normal_speed = True

        if not main_game.game_active:  # Updating the screen
            gamedone_loop(len(main_game.snake.body) - 3, time_elapsed, main_game)  # Calculating the final score and time
            break

        pygame.display.update()
        clock.tick(60)  # Limiting the loop (and the game) to 60 fps


def twoplayer_loop():
    main_game = Main(True)  # An object that will be used to follow the game and execute commands
    time_start = pygame.time.get_ticks()  # storing time at start to calculate run time
    while True:  # Infinite loop I will break when I want the game to stop
        for event in pygame.event.get():  # When starting the game we check for all events
            if event.type == pygame.QUIT:  # If the user closes the window, quit the program
                pygame.quit()
                sys.exit()  # Halting the code
            if event.type == SCREEN_UPDATE:  # Moving the snake constantly when updating the screen
                main_game.update()
            # Defining direction by input and preventing changing direction by 180 degrees
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.next_direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.next_direction = Vector2(0, 1)
                if event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.next_direction = Vector2(1, 0)
                if event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.next_direction = Vector2(-1, 0)
                if event.key == pygame.K_w:
                    if main_game.snake2.direction.y != 1:
                        main_game.snake2.next_direction = Vector2(0, -1)
                if event.key == pygame.K_s:
                    if main_game.snake2.direction.y != -1:
                        main_game.snake2.next_direction = Vector2(0, 1)
                if event.key == pygame.K_d:
                    if main_game.snake2.direction.x != -1:
                        main_game.snake2.next_direction = Vector2(1, 0)
                if event.key == pygame.K_a:
                    if main_game.snake2.direction.x != 1:
                        main_game.snake2.next_direction = Vector2(-1, 0)

                if event.key == pygame.K_r:
                    main_game = Main()  # Restarting the game if the input is r
                elif event.key == pygame.K_ESCAPE:
                    main_game.close_game()

        screen.fill((175, 215, 70))
        # Storing time elapsed to calculate whether powerup should be spawned
        time_elapsed = (pygame.time.get_ticks() - time_start) / 1000
        main_game.draw_elements()
        main_game.power_up.draw_check(time_elapsed)  # The function takes the play time
        if not main_game.game_active:  # Updating the screen
            # Calculating final score and time for two players
            score = len(main_game.snake.body) - 3 + len(main_game.snake2.body) - 3
            gamedone_loop(score, time_elapsed, main_game)
            break

        pygame.display.update()
        clock.tick(60)  # Limiting the loop (and the game) to 60 fps


menu_loop()