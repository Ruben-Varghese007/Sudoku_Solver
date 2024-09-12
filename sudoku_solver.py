import pygame
import random
import time

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 540, 540
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver (Backtracking)")

# Colors
OFFWHITE = (225, 225, 225)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 128, 255)
RED = (255, 0, 0)
LIGHTGREEN = (144, 238, 144)
GRAY = (128, 128, 128)

# Set the font
FONT = pygame.font.SysFont('comicsans', 40)

# Draw the grid
def draw_grid():
    gap = WIDTH // 9
    for i in range(10):
        if i % 3 == 0:
            thickness = 4
        else:
            thickness = 1
        pygame.draw.line(WIN, OFFWHITE, (i * gap, 0), (i * gap, HEIGHT), thickness)
        pygame.draw.line(WIN, OFFWHITE, (0, i * gap), (WIDTH, i * gap), thickness)

# Draw numbers and dots on the grid
def draw_numbers(grid, original_grid):
    gap = WIDTH // 9
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                # Render the number in blue if it was part of the original puzzle, else in green
                color = GREEN if original_grid[i][j] != 0 else LIGHTGREEN
                text = FONT.render(str(grid[i][j]), True, color)
            else:
                # Render the dot
                text = FONT.render(".", True, GRAY)
            
            # Get the rect for the text and center it within the grid cell
            text_rect = text.get_rect(center=(j * gap + gap // 2, i * gap + gap // 2))
            WIN.blit(text, text_rect)

# Update the window
def update_window(grid, original_grid):
    WIN.fill(BLACK)
    draw_grid()
    draw_numbers(grid, original_grid)
    pygame.display.update()

# Check if the number can be placed in a given cell
def is_safe(grid, row, col, num):
    for x in range(9):
        if grid[row][x] == num or grid[x][col] == num:
            return False

    # Check the 3x3 box
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False
    return True

# Recursive function to solve sudoku with pygame visualization
def solve_sudoku_visual(grid, original_grid):
    empty = find_empty_location(grid)
    if not empty:
        return True  # No empty space means puzzle is solved
    row, col = empty

    for num in range(1, 10):
        if is_safe(grid, row, col, num):
            grid[row][col] = num
            update_window(grid, original_grid)

            # Check for events like window close while solving
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            time.sleep(0.1)  # Delay for visualization
            
            if solve_sudoku_visual(grid, original_grid):
                return True
            
            # Backtrack
            grid[row][col] = 0
            update_window(grid, original_grid)

            # Check for events again during backtracking
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            time.sleep(0.1)  # Delay for backtracking visualization

    return False


# Find an empty location in the grid
def find_empty_location(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return None

# Generate a random sudoku puzzle and return both the puzzle and the original grid
def generate_sudoku():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    original_grid = [[0 for _ in range(9)] for _ in range(9)]
    
    for _ in range(random.randint(10, 20)):  # Fill random cells
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        num = random.randint(1, 9)
        if is_safe(grid, row, col, num):
            grid[row][col] = num
            original_grid[row][col] = num  # Store the original numbers
    
    return grid, original_grid

# Main function
def main():
    puzzle, original_grid = generate_sudoku()
    run = True
    solved = False
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        if not solved:
            update_window(puzzle, original_grid)
            solve_sudoku_visual(puzzle, original_grid)
            solved = True

    pygame.quit()

if __name__ == "__main__":
    main()
