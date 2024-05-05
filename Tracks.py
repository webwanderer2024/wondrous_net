def search(start, finish, cols_in_left_rows, cols_constr, left_rows_constr, right_rows_constr):
    """Function that can find a path in the grid for the puzzle Tracks from MUMS Puzzle Hunt 2008 competition.
       English - https://wondrousnet.blogspot.com/2024/05/solution-to-puzzle-tracks.html
       Russian - https://wondrousnet.blogspot.com/2024/04/blog-post.html
       Input:
           start - tuple of two integers: start cell from the grid, that has non-zero constraints for its col and row;
           finish - tuple of two integers: finish cell from the grid;
           cols_in_left_rows - integer: number of cols in the left part of the grid;
           cols_constr - tuple of integers: constraints for cols of the grid;
           left_rows_constr - tuple of integers: constraints for rows in the left part of the grid;
           right_rows_constr - tuple of integers: constraints for rows in the right part of the grid.
       Output:
           if search is successful, function will return tuple of tuples of two integers: path from the start cell to the finish cell;
           otherwise function will return False."""
    # compute number of cols and rows in the grid
    num_cols, num_rows = len(cols_constr), len(left_rows_constr)
    start_col, start_row = start[0], start[1]
    # set active and inactive rows constraints for the start cell
    if start_col < cols_in_left_rows:
        active_rows_constr = left_rows_constr
        inactive_rows_constr = right_rows_constr
    else:
        active_rows_constr = right_rows_constr
        inactive_rows_constr = left_rows_constr
    # update constraints for the start cell
    updated_cols_constr = update_constr(cols_constr, start_col)
    updated_active_rows_constr = update_constr(active_rows_constr, start_row)
    path = depth_first_search(start, finish, num_cols, num_rows, cols_in_left_rows,updated_cols_constr, updated_active_rows_constr, inactive_rows_constr, ())
    return path

def depth_first_search(current_cell, finish, num_cols, num_rows, cols_in_left_rows, cols_constr, active_rows_constr, inactive_rows_constr, current_path):
    """Function that performs depth-first search in the grid from a current cell to the finish cell, according to the given constraints.
       Input:
           current_cell - tuple of two integers: current cell of search;
           finish - tuple of two integers: goal cell of search;
           num_cols - integer: number of cols in the grid;
           num_rows - integer: number of rows in the grid;
           cols_in_left_rows - integer: number of cols in the left part of the grid;
           cols_constr - tuple of integers: constraints for cols of the grid;
           active_rows_constr - tuple of integers: active constraints for rows of the grid;
           inactive_rows_constr - tuple of integers: inactive constraints for rows of the grid;
           current_path - tuple of tuples of two integers: path made so far from the start cell.
       Output:
           if search is successful, function will return tuple of tuples of two integers: path from the start cell to the finish cell;
           otherwise function will return False."""
    current_path += (current_cell,)
    # if current cell is a finish cell and constraints satisfied, than path is found;
    # it is sufficient to check only constraints for cols, because if they are satisfied, than constraints for rows are also satisfied
    if current_cell == finish and satisfied(cols_constr):
        return current_path
    else:
        # find adjacent cells for the current cell with corresponding constraints
        adjacent_cells_with_constr = find_adjacent_cells_with_constr(current_cell, finish, num_cols, num_rows, cols_in_left_rows,
                                                                     cols_constr, active_rows_constr, inactive_rows_constr)
        for (adjacent_cell, next_cols_constr, next_active_rows_constr, next_inactive_rows_constr) in adjacent_cells_with_constr:
            # we assume, that path is acyclic
            if adjacent_cell not in current_path:
                path = depth_first_search(adjacent_cell, finish, num_cols, num_rows, cols_in_left_rows,
                                          next_cols_constr, next_active_rows_constr, next_inactive_rows_constr, current_path)
                if path != False:
                    return path
    return False
        
def update_constr(constr, index):
    """Function that update value of constraints for the given index: it will be smaller by one after that.
       Input:
           constr - tuple of integers: constraints for cols or rows of the grid;
           index - integer: index of the updated value.
       Output:
           tuple of integers: updated constraints."""
    updated_value = constr[index] - 1
    updated_constr = constr[:index] + (updated_value,) + constr[index+1:]
    return updated_constr

def satisfied(constr):
    """Function that checks satisfaction of the given constraints.
       Input:
           constr - tuple of integers: constraints for cols or rows of the grid.
       Output:
           if all values of constraints equal to zero, function will return True;
           otherwise function will return False."""
    for value in constr:
        if value != 0:
            return False
    return True

def find_adjacent_cells_with_constr(cell, finish, num_cols, num_rows, cols_in_left_rows, cols_constr, active_rows_constr, inactive_rows_constr):
    """Function that for a given cell, in accordance with the given constraints, will find set of possible adjacent cells, perspective for subsequent search,
       with constraints, corresponding to passage to that cells.
       Input:
           cell - tuple of two integers: given cell;
           finish - tuple of two integers: finish cell;
           num_cols - integer: number of cols in the grid;
           num_rows - integer: number of rows in the grid;
           cols_in_left_rows - integer: number of cols in the left part of the grid;
           cols_constr - tuple of integers: constraints for cols of the grid;
           active_rows_constr - tuple of integers: active constraints for rows of the grid;
           inactive_rows_constr - tuple of integers: inactive constraints for rows of the grid.
       Output:
           tuple of tuples, each of which consits of four parts:
               1) tuple of two integers: adjacent cell;
               2) tuple of integers: constraints for cols of the grid, corresponding to passage to that cell;
               3) tuple of integers: active constraints for rows of the grid, corresponding to passage to that cell;
               4) tuple of integers: inactive constraints for rows of the grid, corresponding to passage to that cell."""
    cell_col, cell_row = cell[0], cell[1]
    adjacent_cells_with_constr = ()
    for direction in ('horizontal','vertical'):
        for move in (+1,-1):
            active_rows_constr_for_move = active_rows_constr
            inactive_rows_constr_for_move = inactive_rows_constr
            if direction == 'horizontal':
                next_col = cell_col + move
                #next col is inside grid
                if next_col >= 0 and next_col < num_cols:
                    next_row = cell_row
                else:
                    continue
                # we move from the left part of the grid to the right, or from right to the left;
                # so we should swap active and inactive constraints for rows
                if (cell_col == cols_in_left_rows - 1 and move == +1) or (cell_col == cols_in_left_rows and move == -1):
                    active_rows_constr_for_move, inactive_rows_constr_for_move = inactive_rows_constr_for_move, active_rows_constr_for_move                    
            elif direction == 'vertical':
                next_row = cell_row + move
                # next row is inside grid
                if next_row >=0 and next_row < num_rows:
                    next_col = cell_col
                else:
                    continue
            # extract values of constraints for the next col and next row
            next_col_value = cols_constr[next_col]
            next_row_value = active_rows_constr_for_move[next_row]
            if next_col_value > 0 and next_row_value > 0:

                # if value of constraints for the next col will be zero after update,
                # and there is some col on the direction, opposite to the finish cell from the next col, with non-zero value of constraints,
                # than this path can't led to solution and should be abandoned
                if next_col_value == 1:
                    finish_col = finish[0]
                    if (next_col <= finish_col and not satisfied(cols_constr[:next_col]) or (next_col >= finish_col and not satisfied(cols_constr[next_col+1:]))):
                        continue

                # if value of active constraints for the next row will be zero after update,
                # and value of inactive constraints for that row is also equal to zero,
                # and there is some row on the direction, opposite to the finish cell from the next row, with non-zero value of active or inactive constraints,
                # than this path can't led to solution and should be abandoned
                if next_row_value == 1 and inactive_rows_constr_for_move[next_row] == 0:
                    finish_row = finish[1]
                    if ((next_row <= finish_row and
                        (not satisfied(active_rows_constr_for_move[:next_row]) or not satisfied(inactive_rows_constr_for_move[:next_row])))
                        or
                        (next_row >= finish_row and
                        (not satisfied(active_rows_constr_for_move[next_row+1:]) or not satisfied(inactive_rows_constr_for_move[next_row+1:])))):
                        continue
                    
                adjacent_cell = (next_col, next_row)
                updated_cols_constr = update_constr(cols_constr,next_col)
                updated_active_rows_constr_for_move = update_constr(active_rows_constr_for_move, next_row)
                adjacent_cells_with_constr += ((adjacent_cell, updated_cols_constr, updated_active_rows_constr_for_move, inactive_rows_constr_for_move),)
    return adjacent_cells_with_constr

# number of cols in the left part of the grid
cols_in_left_rows = 8

#constraints for cols of the grid
cols_constr =(3,3,2,1,4,3,2,3,6,3,4,3,5,2,2,3)

#constraints for rows in the left part of the grid
left_rows_constr = (1,1,4,5,6,4)

#constraints for rows in the right part of the grid
right_rows_constr = (5,2,2,7,6,6)

# start cell
start = (0,0)

# finish cell
finish = (15,5)

def extract_message(grid, path):
    """Function that extract message from the given grid according to the given path.
       Input:
           grid - tuple of tuples of the same size, that consist of integers and None-values: representation of the given grid;
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
            if (col,row) in path and isinstance(cell_value, int):
                message += str(cell_value)
            else:
                message += '-'
        # add newline character after each row
        message += '\n'
    return message

# bottom grid from the puzzle
bottom_grid = ((None,None,8,6,None,8,None,None,None,None,None,None,None,2,None,9),
               (None,1,None,3,None,None,None,1,None,7,None,9,None,None,4,None),
               (7,None,4,None,6,None,9,None,5,4,None,3,4,None,1,None),
               (2,5,3,3,None,None,5,None,None,None,5,None,None,8,2,None),
               (None,None,5,None,None,5,None,None,None,5,None,None,6,3,None,None),
               (None,4,None,5,7,None,2,7,8,9,None,8,2,None,None,2))

if __name__ == '__main__':
    # find path in the upper grid and extract and print corresponding message from the bottom grid of the puzzle
    path = search(start, finish, cols_in_left_rows, cols_constr, left_rows_constr, right_rows_constr)
    message = extract_message(bottom_grid, path)
    print(message)
