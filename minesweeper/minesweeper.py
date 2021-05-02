import random
import re

class Board:
    def __init__(self, dim_size, num_boms):
        self.dim_size = dim_size
        self.num_bombs = num_boms

        self.board = self.make_new_board()
        self.assign_values_to_board()

        # Initialize set to store locations already uncovered
        self.dug = set()

    def make_new_board(self):
        # Generate empty board
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]

        # Plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            # Return random integer N so that a <= N <= b 
            loc = random.randint(0, self.dim_size**2 -1)
            # The number of times dim_size goes into loc tells us what row to look at
            row = loc // self.dim_size
            # The remainder tells us what index in that row to look at
            col = loc % self.dim_size

            if board[row][col] == "*":
                # Bomb already planted
                continue

            # Plant a bomb
            board[row][col] = "*"
            bombs_planted += 1

        return board
    
    def assign_values_to_board(self):
        # Assign a number from 1-8, which represents how many neighbouring bombs there are.
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == "*":
                    # If it's already a bomb, don't calculate anything
                    continue
                self.board[r][c] = self.get_num_neighbouring_bombs(r,c)

    def get_num_neighbouring_bombs(self, row, col):
        num_neighbouring_bombs = 0
        # Make sure not to go out of bounds
        for r in range(max(0, row - 1), min(self.dim_size - 1,row + 1) +1):
            for c in range(max(0, col-1), min(self.dim_size - 1, col + 1) + 1):
                if r == row and c == col:
                    # original location - don't check
                    continue
                if self.board[r][c] == "*":
                    num_neighbouring_bombs += 1
        return num_neighbouring_bombs

    def dig(self, row, col):
        self.dug.add((row, col)) # Keep track of where you dug
        if self.board[row][col] == "*":
            return False
        elif self.board[row][col] > 0:
            return True

        for r in range(max(0, row - 1), min(self.dim_size - 1,row + 1) + 1):
            for c in range(max(0, col-1), min(self.dim_size - 1, col + 1) + 1):
                if (r,c) in self.dug:
                    # Don't dig where you've already dug
                    continue
                self.dig(r,c)
        # If our initial dig didn't hit a bomb, we *shouldn't* hit a bomb here
        return True

    def __str__(self):
        # Create a new array that represents what the user would see
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = " "

        string_rep = ""
        # Get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # Print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = "   "
        cells = []
        for idx, col in enumerate(indices):
            format = "%-" + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += "  ".join(cells)
        indices_row += "  \n"

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f"{i} |"
            cells = []
            for idx, col in enumerate(row):
                format = "%-" + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += " |".join(cells)
            string_rep += " |\n"

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + "-"*str_len + "\n" + string_rep + "-"*str_len

        return string_rep

def play(dim_size=10, num_bombs=10):
    # Create the board and plant the bombs
    board = Board(dim_size, num_bombs)

    # Show the user the board and ask for where they want to dig
    # If location is a bomb, show game over message
    # If location is not a bomb, dig recursively until each square is at least next to a bomb
    # Repeat until there are no more places to dig

    safe = True

    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = re.split(",(\\s)*", input("Where would you like to dig? Input as row,col: ")) # "0, 3"
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Invalid location. Try again.")
            continue
        
        # If it's valid, dig
        safe = board.dig(row, col)
        if not safe:
            # Dug a bomb. Game over
            break

    if safe:
        print("Congratulations! You are victorius.")
    else:
        print("SORRY. GAME OVER :(")
        # Reveal the whole board
        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

if __name__ == "__main__":
    play()