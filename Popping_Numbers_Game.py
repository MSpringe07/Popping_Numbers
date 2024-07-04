import random
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def colorize_number(number):
    color_map = {
        1: Fore.RED,
        2: Fore.GREEN,
        3: Fore.BLUE,
        4: Fore.YELLOW,
        5: Fore.MAGENTA,
        6: Fore.CYAN,
        7: Fore.WHITE,
        8: Fore.LIGHTBLACK_EX,
        9: Fore.LIGHTMAGENTA_EX,
        0: Fore.LIGHTGREEN_EX
    }
    return color_map.get(number, '') + str(number) + Style.RESET_ALL

def print_board(board, predictions, use_predictor):
    size = len(board)
    # Print column numbers
    print("    " + "  ".join(f"{i+1:2}" for i in range(size)))
    print("   " + "+---" * size + "+")
    for row in range(size):
        # Print row number
        print(f"{row+1:2} |", end="")
        for col in range(size):
            if use_predictor and predictions[row][col]:
                print(Fore.YELLOW + ' * ' + Style.RESET_ALL, end="|")
            elif board[row][col] is None:
                print("   ", end="|")
            else:
                print(f" {colorize_number(board[row][col])} ", end="|")
        print("\n   " + "+---" * size + "+")

def check_and_pop(board, numbers_used):
    popped = False
    points = 0
    size = len(board)
    
    def calculate_points(length):
        return 100 if length == 3 else 200 if length == 4 else 500
    
    # Temporary marks for clearing
    marks = [[False] * size for _ in range(size)]
    
    # Check rows
    for i in range(size):
        j = 0
        while j < size - 2:
            if board[i][j] is not None and board[i][j] == board[i][j + 1] == board[i][j + 2]:
                length = 3
                while j + length < size and board[i][j] == board[i][j + length]:
                    length += 1
                points += calculate_points(length)
                for k in range(length):
                    marks[i][j + k] = True
                j += length
                popped = True
            else:
                j += 1
        
    # Check columns
    for i in range(size):
        j = 0
        while j < size - 2:
            if board[j][i] is not None and board[j][i] == board[j + 1][i] == board[j + 2][i]:
                length = 3
                while j + length < size and board[j][i] == board[j + length][i]:
                    length += 1
                points += calculate_points(length)
                for k in range(length):
                    marks[j + k][i] = True
                j += length
                popped = True
            else:
                j += 1
    
    # Check diagonals
    for i in range(size - 2):
        for j in range(size - 2):
            if board[i][j] is not None and board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2]:
                length = 3
                while i + length < size and j + length < size and board[i][j] == board[i + length][j + length]:
                    length += 1
                points += calculate_points(length)
                for k in range(length):
                    marks[i + k][j + k] = True
                popped = True
            
            if board[i + 2][j] is not None and board[i + 2][j] == board[i + 1][j + 1] == board[i][j + 2]:
                length = 3
                while i + length < size and j + 2 - length >= 0 and board[i + 2][j] == board[i + length][j + 2 - length]:
                    length += 1
                points += calculate_points(length)
                for k in range(length):
                    marks[i + k][j + 2 - k] = True
                popped = True
    
    # Clear marked cells
    for i in range(size):
        for j in range(size):
            if marks[i][j]:
                board[i][j] = None
                
    return popped, points

def is_full(board):
    return all(cell is not None for row in board for cell in row)

def add_random_numbers(board, numbers_used, predictions, use_predictor):
    size = len(board)
    for _ in range(3):
        if is_full(board):
            return
        while True:
            row = random.randint(0, size - 1)
            col = random.randint(0, size - 1)
            if board[row][col] is None and not (use_predictor and predictions[row][col]):
                board[row][col] = random.choice(numbers_used)
                break
    # Check for lines to clear after adding random numbers
    while True:
        popped, _ = check_and_pop(board, numbers_used)
        if not popped:
            break

def main():
    # Initialize game settings
    while True:
        try:
            size = int(input("Enter board size (5-25): "))
            if size < 5 or size > 25:
                print("Invalid size. Please enter a number between 5 and 25.")
                continue
            
            numbers_used = list(map(int, input("Enter the numbers to be used (separated by space, 0-9): ").split()))
            if not all(0 <= num <= 9 for num in numbers_used) or len(numbers_used) == 0:
                print("Invalid numbers. Please enter numbers between 0 and 9.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
            continue

    while True:
        use_predictor = input("Would you like to use the appearance predictor? (yes/no): ").strip().lower()
        if use_predictor in ['yes', 'no']:
            use_predictor = use_predictor == 'yes'
            break
        print("Invalid input. Please enter 'yes' or 'no'.")

    board = [[None] * size for _ in range(size)]
    predictions = [[False] * size for _ in range(size)]
    player_points = 0
    
    while True:
        print_board(board, predictions, use_predictor)
        print(f"Player Points: {player_points}")
        
        while True:
            try:
                number = int(input(f"Enter a number {numbers_used}: "))
                if number not in numbers_used:
                    print("Invalid number. Try again.")
                    continue
                
                row = int(input(f"Enter the row (1-{size}): ")) - 1
                col = int(input(f"Enter the column (1-{size}): ")) - 1
                
                if row < 0 or row >= size or col < 0 or col >= size or board[row][col] is not None:
                    print("Invalid position. Try again.")
                    continue
                break
            except ValueError:
                print("Invalid input. Try again.")
        
        board[row][col] = number
        predictions[row][col] = False  # Clear the prediction mark for the placed number

        while True:
            popped, points = check_and_pop(board, numbers_used)
            if not popped:
                break
            player_points += points

        print_board(board, predictions, use_predictor)  # Show the board after player's move

        if is_full(board):
            print(f"Game Over! Final Player Points: {player_points}")
            break

        add_random_numbers(board, numbers_used, predictions, use_predictor)

        # Check and clear lines after adding random numbers without awarding points
        while True:
            popped, _ = check_and_pop(board, numbers_used)
            if not popped:
                break

        if use_predictor:
            # Clear previous predictions
            predictions = [[False] * size for _ in range(size)]
            # Add new predictions
            for _ in range(3):
                while True:
                    row = random.randint(0, size - 1)
                    col = random.randint(0, size - 1)
                    if board[row][col] is None:
                        predictions[row][col] = True
                        break

if __name__ == "__main__":
    main()
