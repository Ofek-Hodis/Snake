import pygame  # Importing pygame for the creation of the game
import json


def text_draw(text, position, title_font, size, color, screen):
    font = pygame.font.Font(title_font, size)
    title_text = font.render(text, True, color)
    title_rect = title_text.get_rect(center=position)
    screen.blit(title_text, title_rect)


def get_high_score():
    with open("Data/high_score.json", "r") as f:  # Opening the file in read mode to get the top score
        data = json.load(f)  # Turning the data to a Python dictionary

    high_score = data["high_score"]
    return high_score


def store_high_score(new_score):
    with open("Data/high_score.json", "w") as f:  # Opening the file in write mode to update the score
        json.dump({"high_score": new_score}, f)  # Converting the text to JSON form and writing it into the file



