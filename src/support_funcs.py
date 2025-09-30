import pygame  # Importing pygame for the creation of the game
import json  # Importing JSON for high score tracking and update purposes


def text_draw(text, position, title_font, size, color, screen):
    font = pygame.font.Font(title_font, size)  # Setting up the given font to be a pygame font
    title_text = font.render(text, True, color)
    title_rect = title_text.get_rect(center=position)  # Creating a rectangle to place the title in it's center
    screen.blit(title_text, title_rect)


def get_high_score():
    with open("Data/high_score.json", "r") as f:  # Opening the file in read mode to get the top score
        data = json.load(f)  # Turning the data to a Python dictionary

    high_score = data["single_high_score"]  # Saving the data from JSON file to a variable
    return high_score


def get_high_score_twoplayer():
    with open("Data/high_score.json", "r") as f:  # Opening the file in read mode to get the top score
        data = json.load(f)  # Turning the data to a Python dictionary

    high_score = data["two_player_high_score"]  # Saving the data from JSON file to a variable
    return high_score


def store_high_score(new_score):
    with open("Data/high_score.json", "r+") as f:  # Opening the file in read & write mode to update the score
        data = json.load(f)  # Turning the data to a Python dictionary
        two_score = data["two_player_high_score"]  # Storing two player high score
        f.seek(0)  # Returning the pointer to the first place of the array
        # Converting the text to JSON form and writing it into the file
        json.dump({"single_high_score": new_score, "two_player_high_score": two_score}, f)


def store_high_score_twoplayer(new_score):
    with open("Data/high_score.json", "r+") as f:  # Opening the file in read & write mode to update the score
        data = json.load(f)  # Turning the data to a Python dictionary
        single_score = data["single_high_score"]  # Storing two player high score
        f.seek(0)
        # Converting the text to JSON form and writing it into the file
        json.dump({"single_high_score": single_score, "two_player_high_score": new_score}, f)

