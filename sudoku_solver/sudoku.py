from pprint import pprint

def find_next_empty(puzzle):
    # Finds the next row, col on the puzzle that's not filled yet --> rep with -1
    # Returns row, col tuple (or (None, None) if there is none)

    # Keep in mind that we are using 0-8 for our indices
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == -1:
                return r, c
    return None, None # If no spaces in the puzzle are empty (-1)

def is_valid(puzzle, guess, row, col):
    # Figures out whether the guess at the row/col of the puzzle is a valid guess
    # Returns True or False

    # For a guess to be valid, then we need to follow the sudoku rules
    # That number must not be repeated in the row, column, or 3x3 square that it appears in

    row_vals = puzzle[row]
    if guess in row_vals:
        return False # If we've repeated, then our guess is not valid

    # col_vals = []
    # for i in range(9):
    #     col_vals.append(puzzle[i][col])
    col_vals = [puzzle[i][col] for i in range(9)]
    if guess in col_vals:
        return False 

    row_start = (row // 3) * 3
    col_start = (col // 3) * 3

    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if puzzle[r][c] == guess:
                return False

    return True

def solve_sudoku(puzzle):
    # Solve sudoku using backtracking
    # Our puzzle is a list of lists, where each inner list is a row in our sudoku puzzle
    # Return whether a solution exists
    # Mutates puzzle to be the solution (if solution exists)
    
    # Step 1: choose somewhere on the puzzle to make a guess
    row, col = find_next_empty(puzzle)

    # Step 1.1: If there's nowhere left, then we're done because we only allowed valid inputs
    if row is None: # This is true if our find_next_empty function returns None, None
        return True
    
    # Step 2: If there is a place to put a number, then make a guess between 1 and 9
    for guess in range(1,10):
        # Step 3: Check if this is a valid guess
        if is_valid(puzzle, guess, row, col):
            # Step 3.1: If this is a valid guess, then place it at that spot on the puzzle
            puzzle[row][col] = guess
            # Step 4: Then we recursively call our solver
            if solve_sudoku(puzzle):
                return True
    
        # Step 5: It not valid or if nothing gets returned true, then we need to backtrack and try a new number
        puzzle[row][col] = -1

    # Step 6: If none of the numbers that we try work, then this puzzle is unsolveable
    return False

if __name__ == "__main__":
    example_board = [
        [3, 9, -1,   -1, 5, -1,   -1, -1, -1],
        [-1, -1, -1,   2, -1, -1,   -1, -1, 5],
        [-1, -1, -1,   7, 1, 9,   -1, 8, -1],

        [-1, 5, -1,   -1, 6, 8,   -1, -1, -1],
        [2, -1, 6,   -1, -1, 3,   -1, -1, -1],
        [-1, -1, -1,   -1, -1, -1,   -1, -1, 4],

        [5, -1, -1,   -1, -1, -1,   -1, -1, -1],
        [6, 7, -1,   1, -1, 5,   -1, 4, -1],
        [1, -1, 9,   -1, -1, -1,   2, -1, -1]
    ]
print(solve_sudoku(example_board))
pprint(example_board)