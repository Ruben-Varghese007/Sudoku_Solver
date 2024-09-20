import streamlit as st
import random
import time

# Set up the Streamlit page
st.title("Sudoku Solver (Backtracking)")
st.write("This app generates a random Sudoku puzzle or solves an existing one using Backtracking Algorithm.")
st.write("Name:  [ Ruben George Varghese ]")
st.write("GitHub: [ https://github.com/Ruben-Varghese007/Sudoku_Solver ]")
st.divider()

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

# Initialize grid and placeholders
def initialize_grid():
    return [[0 for _ in range(9)] for _ in range(9)]

# Validate Sudoku grid for duplicates in rows, columns, and 3x3 boxes
def validate_sudoku(grid):
    def has_duplicates(seq):
        seq = [num for num in seq if num != 0]
        return len(seq) != len(set(seq))
    
    # Check rows and columns
    for i in range(9):
        if has_duplicates(grid[i]) or has_duplicates([grid[j][i] for j in range(9)]):
            return False
    
    # Check 3x3 subgrids
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            subgrid = [grid[x][y] for x in range(i, i+3) for y in range(j, j+3)]
            if has_duplicates(subgrid):
                return False
    
    return True

# Streamlit app logic
input_method = st.radio("Choose Input Method:", ("Generate Random Puzzle", "Enter Sudoku Puzzle"))

if input_method == "Enter Sudoku Puzzle":
    st.write("Enter your Sudoku puzzle below:")
    st.write("Note: Cell(row,column) - Only enter values between 1 and 9")
    sudoku_grid = initialize_grid()
    
    # Create a 9x9 grid layout
    inputs = []
    for i in range(9):
        row_inputs = st.columns(9)
        row_values = []
        for j in range(9):
            input_key = f"cell_{i}_{j}"
            value = row_inputs[j].text_input("", value='', max_chars=1, key=input_key, help=f"Cell ({i+1},{j+1})")
            row_values.append(value)
        inputs.append(row_values)

    # Validate input values
    def get_grid_from_inputs():
        grid = initialize_grid()
        for i in range(9):
            for j in range(9):
                try:
                    value = int(inputs[i][j])
                    if 1 <= value <= 9:
                        grid[i][j] = value
                except ValueError:
                    pass  # Empty or invalid input treated as 0 (empty cell)
        return grid

    # Convert input values to grid and validate
    if st.button('Solve Sudoku'):
        sudoku_grid = get_grid_from_inputs()
        original_grid = [row[:] for row in sudoku_grid]  # Copy the grid

        # Check if the entire grid is empty
        if all(sudoku_grid[i][j] == 0 for i in range(9) for j in range(9)):
            st.error("Please enter at least one number in the Sudoku grid.")
        # Check if the entered values are valid
        elif not validate_sudoku(sudoku_grid):
            st.error("Invalid Sudoku grid. Please correct your input.")
        else:
            grid_placeholder = st.empty()
            display_grid(sudoku_grid, grid_placeholder, original_grid)

            # Add some vertical space between the puzzle and the message
            st.markdown("<br>", unsafe_allow_html=True)

            if solve_sudoku_visual(sudoku_grid, grid_placeholder, original_grid):
                st.success("Sudoku solved!")
            else:
                st.error("Failed to solve the Sudoku puzzle.")

elif input_method == "Generate Random Puzzle":
    if st.button('Generate and Solve Sudoku'):
        puzzle = generate_sudoku()
        original_grid = [row[:] for row in puzzle]  # Copy the puzzle
        grid_placeholder = st.empty()
        display_grid(puzzle, grid_placeholder, original_grid)
        st.markdown("<br>", unsafe_allow_html=True)
        if solve_sudoku_visual(puzzle, grid_placeholder, original_grid):
            st.success("Sudoku solved!")
        else:
            st.error("Failed to solve the Sudoku puzzle.")
