def search(start, finish, cols_in_left_part, cols_constr, left_rows_constr, right_rows_constr):
    """Function for finding a path in the grid for the puzzle Tracks from MUMS Puzzle Hunt 2008 competition.
       Russian - https://wondrousnet.blogspot.com/2024/04/blog-post.html
       English - https://wondrousnet.blogspot.com/2024/05/solution-to-puzzle-tracks.html
       Input:
           start - tuple of two integers: start cell of the grid;
           finish - tuple of two integers: finish cell of the grid;
           cols_in_left_part - integer: number of cols in the left part of the grid;
           cols_constr - list of integers: constraints for the cols of the grid;
           left_rows_constr - list of integers: constraints for the rows in the left part of the grid;
           right_rows_constr - list of integers: constraints for the rows in the right part of the grid.
       Output:
           if search is successful, the function will return tuple of tuples of two integers: path from the start cell to the finish cell;
           otherwise the function will return False."""
    cols_constr = list(cols_constr)
    left_rows_constr = list(left_rows_constr)
    right_rows_constr = list(right_rows_constr)
    start_col, start_row = start[0], start[1]
    # set active and inactive rows constraints for the start cell
    if start_col < cols_in_left_part:
        active_rows_constr = left_rows_constr
        inactive_rows_constr = right_rows_constr
    else:
        active_rows_constr = right_rows_constr
        inactive_rows_constr = left_rows_constr
    # update constraints according to the start cell
    if cols_constr[start_col] > 0 and active_rows_constr[start_row] > 0:
        cols_constr[start_col] -= 1
        active_rows_constr[start_row] -= 1
    else:
        raise ValueError("Start cell shoud have non-zero values of constraints.")
    path = depth_first_search((start,), finish, cols_in_left_part, cols_constr, active_rows_constr, inactive_rows_constr)
    return path

def depth_first_search(path, finish, cols_in_left_part, cols_constr, active_rows_constr, inactive_rows_constr):
    """Function that performs depth-first search in the grid from a current cell to the finish cell according to the given constraints.
       Input:
           path - tuple of tuples of two integers: path made so far from the start cell;
           finish - tuple of two integers: goal cell of search;
           cols_in_left_part - integer: number of cols in the left part of the grid;
           cols_constr - list of integers: constraints for the cols of the grid;
           active_rows_constr - list of integers: active constraints for the rows of the grid;
           inactive_rows_constr - list of integers: inactive constraints for the rows of the grid.
       Output:
           if search is successful, the function will return tuple of tuples of two integers: path from the start cell to the finish cell;
           otherwise the function will return False."""
    current_cell = path[-1]
    # if current cell is a finish cell and constraints are satisfied, than path is found
    if current_cell == finish and sum(cols_constr) == 0:
        return path
    # find perspective adjacent cells for the current cell with corresponding constraints
    next_state = get_next_state(current_cell, finish, cols_in_left_part, cols_constr, active_rows_constr, inactive_rows_constr)
    for (adjacent_cell, next_cols_constr, next_active_rows_constr, next_inactive_rows_constr) in next_state:
        # we assume, that path is acyclic
        if adjacent_cell not in path:
            extended_path = path + (adjacent_cell,)
            final_path = depth_first_search(extended_path, finish, cols_in_left_part, next_cols_constr, next_active_rows_constr, next_inactive_rows_constr)
            if final_path:
                return final_path
    return False
        
def get_next_state(cell, finish, cols_in_left_part, cols_constr, active_rows_constr, inactive_rows_constr):
    """Function that for the given cell, in accordance with the given constraints, generate possible adjacent cells, perspective for subsequent search,
       with constraints, corresponding to passage to that cells.
       Input:
           cell - tuple of two integers: given cell;
           finish - tuple of two integers: finish cell;
           cols_in_left_part - integer: number of cols in the left part of the grid;
           cols_constr - list of integers: constraints for the cols of the grid;
           active_rows_constr - list of integers: active constraints for the rows of the grid;
           inactive_rows_constr - list of integers: inactive constraints for the rows of the grid.
       Output:
           generator that will yield tuples of four elements:
               1) tuple of two integers: adjacent cell;
               2) list of integers: constraints for the cols of the grid, corresponding to passage to that cell;
               3) list of integers: active constraints for the rows of the grid, corresponding to passage to that cell;
               4) list of integers: inactive constraints for the rows of the grid, corresponding to passage to that cell."""
    num_cols = len(cols_constr)
    num_rows = len(active_rows_constr)
    col, row = cell[0], cell[1]
    for direction in ('horizontal','vertical'):
        for move in (+1,-1):
            next_active_rows_constr = active_rows_constr
            next_inactive_rows_constr = inactive_rows_constr
            if direction == 'horizontal':
                next_col = col + move
                #next col is inside grid
                if next_col >= 0 and next_col < num_cols:
                    next_row = row
                else:
                    continue
                # we move from the left part of the grid to the right, or from right to the left;
                # so we should swap active and inactive constraints for the rows
                if (col == cols_in_left_part - 1 and move == +1) or (col == cols_in_left_part and move == -1):
                    next_active_rows_constr, next_inactive_rows_constr = next_inactive_rows_constr, next_active_rows_constr                 
            elif direction == 'vertical':
                next_row = row + move
                # next row is inside grid
                if next_row >=0 and next_row < num_rows:
                    next_col = col
                else:
                    continue
            # extract values of constraints for the next col and next row
            next_col_value = cols_constr[next_col]
            next_row_value = next_active_rows_constr[next_row]
            # constraints are allow to make the move
            if next_col_value > 0 and next_row_value > 0:
                # if value of constraints for the next col will be zero after move,
                # and there is some col before the next col and finish col or after the next col and finish col
                # with non-zero value of constraints,
                # than this path can't led to solution and should be abandoned
                if next_col_value == 1:
                    finish_col = finish[0]
                    if (next_col <= finish_col and sum(cols_constr[:next_col])>0
                        or
                        next_col >= finish_col and sum(cols_constr[next_col+1:])>0):
                        continue
                # if value of active constraints for the next row will be zero after move,
                # and value of inactive constraints for that row is also equal to zero,
                # and there is some row before the next row and finish row or after the next row and finish row
                # with non-zero value of active or inactive constraints,
                # than this path can't led to solution and should be abandoned
                if next_row_value == 1 and next_inactive_rows_constr[next_row] == 0:
                    finish_row = finish[1]
                    if (next_row <= finish_row and
                        (sum(next_active_rows_constr[:next_row])>0 or sum(next_inactive_rows_constr[:next_row])>0)
                        or
                        next_row >= finish_row and
                        (sum(next_active_rows_constr[next_row+1:])>0 or sum(next_inactive_rows_constr[next_row+1:])>0)):
                        continue                   
                adjacent_cell = (next_col, next_row)
                next_cols_constr = list(cols_constr)
                next_active_rows_constr = list(next_active_rows_constr)
                next_cols_constr[next_col] -= 1
                next_active_rows_constr[next_row] -= 1
                yield (adjacent_cell, next_cols_constr, next_active_rows_constr, next_inactive_rows_constr)

# number of cols in the left part of the grid
cols_in_left_part = 8

#constraints for the cols of the grid
cols_constr =[3,3,2,1,4,3,2,3,6,3,4,3,5,2,2,3]

#constraints for the rows in the left part of the grid
left_rows_constr = [1,1,4,5,6,4]

#constraints for the rows in the right part of the grid
right_rows_constr = [5,2,2,7,6,6]

# start cell
start = (0,0)

# finish cell
finish = (15,5)

def extract_message(grid, path):
    """Function that extract message from the given grid according to the given path.
       Input:
           grid - tuple of tuples of the same size, that consist of integers:
                  representation of the given grid, where 0 denotes an empty cell;
           path - tuple of tuples of two integers: path from the corresponding grid of the puzzle.
       Output:
           string - exctracted message: if path moved through a cell of the grid and that cell is not empty,
           than the message will have a number from that cell in the corresponding place,
           otherwise there will be '-' character on that place."""
    num_rows = len(grid)
    num_cols = len(grid[0])
    message = ''
    # decremental loop for the number of rows
    for row in range(num_rows-1,-1,-1):
        for col in range(num_cols):
            cell_value = grid[row][col]
            if cell_value > 0 and (col,row) in path:
                message += str(cell_value)
            else:
                message += '-'
        # add newline character after each row
        message += '\n'
    return message

# bottom grid from the puzzle, where 0 denotes an empty cell
bottom_grid = ((0,0,8,6,0,8,0,0,0,0,0,0,0,2,0,9),
               (0,1,0,3,0,0,0,1,0,7,0,9,0,0,4,0),
               (7,0,4,0,6,0,9,0,5,4,0,3,4,0,1,0),
               (2,5,3,3,0,0,5,0,0,0,5,0,0,8,2,0),
               (0,0,5,0,0,5,0,0,0,5,0,0,6,3,0,0),
               (0,4,0,5,7,0,2,7,8,9,0,8,2,0,0,2))

if __name__ == '__main__':
    # find path in the upper grid and extract and print corresponding message from the bottom grid of the puzzle
    path = search(start, finish, cols_in_left_part, cols_constr, left_rows_constr, right_rows_constr)
    message = extract_message(bottom_grid, path)
    print(message)
