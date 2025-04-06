"""
This program simulates the game of tic tac toe.
"""

# Get a valid row or column index from the user (0, 1, or 2)
def get_valid_index(prompt):
    while True:
        try:
            index = int(input(prompt))
            if 0 <= index <= 2:
                return index
            else:
                print("Input must be a number between 0 and 2 (inclusive).")
        except ValueError:
            print("Invalid input. Please enter an integer between 0 and 2.")

# Return True if the game is over, False otherwise. Print the result.
def game_is_over(board):
    for i in range(3):
        # Check rows
        if board[i][0] == board[i][1] == board[i][2] != " ":
            print_board(board)
            print(f"{board[i][0]} wins!")
            return True

        # Check columns
        if board[0][i] == board[1][i] == board[2][i] != " ":
            print_board(board)
            print(f"{board[0][i]} wins!")
            return True

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != " ":
        print_board(board)
        print(f"{board[0][0]} wins!")
        return True

    if board[0][2] == board[1][1] == board[2][0] != " ":
        print_board(board)
        print(f"{board[0][2]} wins!")
        return True

    # Check for tie
    if all(cell != " " for row in board for cell in row):
        print_board(board)
        print("It's a tie!")
        return True

    return False  # Game is not over

# Print the current board
def print_board(board):
    print("\nCurrent board:")
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

# Initialize the board
board = [[" " for _ in range(3)] for _ in range(3)]
turn = "x"  # x goes first

# Main game loop
while not game_is_over(board):
    print_board(board)
    print(f"It's {turn}'s turn.")

    while True:
        row = get_valid_index("Enter row (0-2): ")
        col = get_valid_index("Enter column (0-2): ")

        if board[row][col] == " ":
            board[row][col] = turn
            turn = "o" if turn == "x" else "x"
            break
        else:
            print("That space is already taken. Try again.")

