# Snake
A snake game with speed altering powerups and a two-player function created using **Python** and **Pygame**, following object oriented principles.
This project was created to practice game loops, class creation and usage, collision detection and menu creation using Pygame.

---

## Preview
<img width="500" height="500" alt="main_menu" src="https://github.com/user-attachments/assets/b64141db-1e88-4b85-9311-d64ab2e04a0b" />

<img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/8879db4a-a4d6-490f-8d0e-440e3cbc69fe" />

<img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/f9732243-23a1-4948-b0c0-5240226c6fbc" />

<img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/7341f87c-6093-46c6-8553-2a1a11b0752e" />

---

## Features
- Classic snake features (collision detection, fruit collection, snake growth
- Two-player mode with collisions checks between snakes
- Menus (Main menu and game over menu allowing acces to single-player mode and two-player mode using buttons
- Time and score tracking (as well as high score tracking for each mode using a JSON file)
- Speed changing power ups (randomly spawning and altering game-speed when collected)
- Various sound effects (Fruit eaten, game over, powerup consumed, etc.)

---

## Requirements
Python 3.10+ (Developped and tested on Python 3.13.7)
Pygame 2.1.0+ (Developped and tested on version 2.6.1)


---

## Installation
1. Clone the repository:
  git clone https://github.com/Ofek-Hodis/Snake
  cd Snake
2. Install requirements (see above)
  Example:
    pip install pygame
3. Run the game:
   Python main.py

---

## Controls
For single-player arrow-keys control the snake, use esc to close the game at any time.
For two-player mode, the same controls apply. Use wasd to control the second snake.

---

## Gameplay

### Single Player
- Control the snake using arrow keys.
- Eat apples and grow to increase your score.
- Eat powerups (marked by the purple questionmark) for a change of speed.
- Game ends if you collide with the walls or yourself.

### Two=-player
- Blue snake: control using **arrow keys**, can only eat **apples**.
- Red snake: control using **WASD**, can only eat **oranges**.
- Eat powerups (marked by the purple questionmark) for a change of speed.
- If a snake tries to eat the other snake's fruit, it's location will be randomized without the score and the size of the snake increasing.
- Game ends if either snake collides with the other, the walls or itself.


## Project Structure

PLACEHOLDER

---

## Possible Future Improvements
- Add pause/resume functionality.
- Add 3 player game-mode.
- Additional power-ups.
- Background music.
