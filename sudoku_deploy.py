import streamlit as st
import random
import time

# Set up the Streamlit page
st.title("Sudoku Solver (Brute Force)")
st.write("This app generates a random Sudoku puzzle and solves it using a Backtracking Algorithm.")

# Function to display Sudoku grid in Streamlit with color differentiation
def display_grid(grid, grid_placeholder, original_grid):
    grid_html = "<table style='border-collapse: collapse; font-size: 30px; margin: auto;'>"
    
    for i in range(9):
        grid_html += "<tr>"
        for j in range(9):
            cell_value = str(grid[i][j]) if grid[i][j] != 0 else "."
            
            # Color logic: original cells in blue, filled-in cells in green, empty in red
            if original_grid[i][j] != 0:
                cell_color = "green"  # Pre-filled random numbers
            elif grid[i][j] != 0:
                cell_color = "lightgreen"  # Numbers added during solving
            else:
                cell_color = "lightred"  # Empty cells
            
            # Thicker borders for every 3x3 subgrid
            border_bottom = "4px solid white" if (i + 1) % 3 == 0 else "1px solid white"
            border_right = "4px solid white" if (j + 1) % 3 == 0 else "1px solid white"

            # Add thicker borders to the outermost edges of the grid
            border_top = "4px solid white" if i == 0 else "1px solid white"
            border_left = "4px solid white" if j == 0 else "1px solid white"

            if i == 8:
                border_bottom = "4px solid white"
            
            if j == 8:
                border_right = "4px solid white"
            
            # Combine all borders
            grid_html += f"<td style='border-top: {border_top}; border-left: {border_left}; border-bottom: {border_bottom}; border-right: {border_right}; width: 50px; height: 50px; text-align: center; color: {cell_color};'>{cell_value}</td>"
        
        grid_html += "</tr>"
    
    grid_html += "</table>"

    # Use HTML to render the grid
    grid_placeholder.markdown(grid_html, unsafe_allow_html=True)

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

# Recursive function to solve sudoku with Streamlit visualization
def solve_sudoku_visual(grid, grid_placeholder, original_grid):
    empty = find_empty_location(grid)
    if not empty:
        return True  # No empty space means puzzle is solved
    row, col = empty

    for num in range(1, 10):
        if is_safe(grid, row, col, num):
            grid[row][col] = num
            display_grid(grid, grid_placeholder, original_grid)
            time.sleep(0.1)  # Delay for visualization
            
            if solve_sudoku_visual(grid, grid_placeholder, original_grid):
                return True
            
            # Backtrack
            grid[row][col] = 0
            display_grid(grid, grid_placeholder, original_grid)
            time.sleep(0.1)  # Delay for backtracking visualization

    return False

# Find an empty location in the grid
def find_empty_location(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return None

# Generate a random sudoku puzzle
def generate_sudoku():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    for _ in range(random.randint(10, 20)):  # Fill random cells
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        num = random.randint(1, 9)
        if is_safe(grid, row, col, num):
            grid[row][col] = num
    return grid

# Streamlit app logic
if st.button('Generate and Solve Sudoku'):
    # Generate the puzzle
    puzzle = generate_sudoku()
    
    # Store the original grid for color differentiation
    original_grid = [row[:] for row in puzzle]  # Copy the puzzle

    # Placeholder for the grid to keep updating it
    grid_placeholder = st.empty()
    
    # Display the initial puzzle
    display_grid(puzzle, grid_placeholder, original_grid)

    # Add some vertical space between the puzzle and the message
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Attempt to solve the puzzle with a brute force approach
    if solve_sudoku_visual(puzzle, grid_placeholder, original_grid):
        st.success("Sudoku solved!")
    else:
        st.error("Failed to solve the Sudoku puzzle.")
