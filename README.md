# Colorful Number Matching Game

This is a simple number matching game implemented in Python. The game uses a board where players place numbers and earn points by aligning three or more identical numbers in a row, column, or diagonal. The numbers are colorized for better visualization using the `colorama` library.

## Features

- Customizable board size (5x5 to 25x25).
- Selectable set of numbers (0-9) to use in the game.
- Optional appearance predictor to mark potential upcoming number placements.
- Automatic clearing of aligned numbers and awarding of points.

## Installation

1. Ensure you have Python installed on your machine.
2. Install the required `colorama` package using pip:
    ```bash
    pip install colorama
    ```

## How to Play

1. Run the game:
    ```bash
    python game.py
    ```

2. Enter the board size (between 5 and 25).
3. Enter the numbers you want to use (between 0 and 9, separated by spaces).
4. Decide if you want to use the appearance predictor by typing 'yes' or 'no'.
5. The game will display the board. Players take turns entering a number and its position on the board.
6. The game automatically checks for and clears any lines of three or more identical numbers, awarding points accordingly.
7. Random numbers are added to the board after each turn.
8. The game ends when the board is full. The player's final points are displayed.

## Functions

### `colorize_number(number)`

Colorizes the given number using `colorama` colors based on a predefined mapping.

### `print_board(board, predictions, use_predictor)`

Prints the current state of the board, highlighting prediction marks if the predictor is enabled.

### `check_and_pop(board, numbers_used)`

Checks the board for any lines of three or more identical numbers and clears them, returning a flag indicating if any numbers were cleared and the points earned.

### `is_full(board)`

Checks if the board is full.

### `add_random_numbers(board, numbers_used, predictions, use_predictor)`

Adds three random numbers to the board, ensuring they do not overlap with predictions if the predictor is enabled. Also checks for lines to clear after adding numbers.

## Game Loop

- Initialize the board and settings.
- Enter a number and its position.
- Check and clear any lines of identical numbers.
- Add random numbers to the board.
- Update and display predictions if the predictor is enabled.
- Repeat until the board is full and display the final score.

