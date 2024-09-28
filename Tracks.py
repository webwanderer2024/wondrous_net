def search(start, finish, cols_in_left_part, cols_constr, left_rows_constr, right_rows_constr):
    """Function for finding a path in the field for the puzzle Tracks from MUMS Puzzle Hunt 2008 competition.
       Russian - https://wondrousnet.blogspot.com/2024/04/blog-post.html
       English - https://wondrousnet.blogspot.com/2024/05/solution-to-puzzle-tracks.html
       Input:
           start - tuple of two integers: start cell of the field;
           finish - tuple of two integers: finish cell of the field;
           cols_in_left_part - integer: number of cols in the left part of the field;
           cols_constr - list or tuple of integers: constraints for the cols of the field;
           left_rows_constr - list or tuple of integers: constraints for the rows in the left part of the field;
           right_rows_constr - list or tuple of integers: constraints for the rows in the right part of the field.
       Output:
           if search is successful, function will return tuple of tuples of two integers: path from the start cell to the finish cell;
           otherwise function will return False."""
    cols_constr = list(cols_constr)
    left_rows_constr = list(left_rows_constr)
    right_rows_constr = list(right_rows_constr)
    # compute number of cols and rows in the field
    num_cols, num_rows = len(cols_constr), len(left_rows_constr)
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
    path = depth_first_search(start, finish, num_cols, num_rows, cols_in_left_part,
                              cols_constr, active_rows_constr, inactive_rows_constr, ())
    return path

def depth_first_search(current_cell, finish, num_cols, num_rows, cols_in_left_part, cols_constr, active_rows_constr, inactive_rows_constr, current_path):
    """Function that performs depth-first search in the field from a current cell to the finish cell, according to the given constraints.
       Input:
           current_cell - tuple of two integers: current cell of search;
           finish - tuple of two integers: goal cell of search;
           num_cols - integer: number of cols in the field;
           num_rows - integer: number of rows in the field;
           cols_in_left_part - integer: number of cols in the left part of the field;
           cols_constr - list of integers: constraints for the cols of the field;
           active_rows_constr - list of integers: active constraints for the rows of the field;
           inactive_rows_constr - list of integers: inactive constraints for the rows of the field;
           current_path - tuple of tuples of two integers: path made so far from the start cell.
       Output:
           if search is successful, the function will return tuple of tuples of two integers: path from the start cell to the finish cell;
           otherwise the function will return False."""
    current_path += (current_cell,)
    # if current cell is a finish cell and constraints satisfied, than path is found;
    # it is sufficient to check only constraints for the cols, because if they are satisfied, than constraints for the rows are also satisfied
    if current_cell == finish and sum(cols_constr) == 0:
        return current_path
    # find adjacent cells for the current cell with corresponding constraints
    adjacent_cells_with_constr = find_adjacent_cells_with_constr(current_cell, finish, num_cols, num_rows, cols_in_left_part,
                                                                 cols_constr, active_rows_constr, inactive_rows_constr)
    for (adjacent_cell, next_cols_constr, next_active_rows_constr, next_inactive_rows_constr) in adjacent_cells_with_constr:
        # we assume, that path is acyclic
        if adjacent_cell not in current_path:
            path = depth_first_search(adjacent_cell, finish, num_cols, num_rows, cols_in_left_part,
                                        next_cols_constr, next_active_rows_constr, next_inactive_rows_constr, current_path)
            if path:
                return path
    return False
        
def find_adjacent_cells_with_constr(cell, finish, num_cols, num_rows, cols_in_left_part, cols_constr, active_rows_constr, inactive_rows_constr):
    """Function that for the given cell, in accordance with the given constraints, will find set of possible adjacent cells, perspective for subsequent search,
       with constraints, corresponding to passage to that cells.
       Input:
           cell - tuple of two integers: given cell;
           finish - tuple of two integers: finish cell;
           num_cols - integer: number of cols in the field;
           num_rows - integer: number of rows in the field;
           cols_in_left_part - integer: number of cols in the left part of the field;
           cols_constr - list of integers: constraints for the cols of the field;
           active_rows_constr - list of integers: active constraints for the rows of the field;
           inactive_rows_constr - list of integers: inactive constraints for the rows of the field.
       Output:
           generator that will yield tuples of four elements:
               1) tuple of two integers: adjacent cell;
               2) list of integers: constraints for the cols of the field, corresponding to passage to that cell;
               3) list of integers: active constraints for the rows of the field, corresponding to passage to that cell;
               4) list of integers: inactive constraints for the rows of the field, corresponding to passage to that cell."""
    col, row = cell[0], cell[1]
    for direction in ('horizontal','vertical'):
        for move in (+1,-1):
            next_active_rows_constr = active_rows_constr
            next_inactive_rows_constr = inactive_rows_constr
            if direction == 'horizontal':
                next_col = col + move
                #next col is inside field
                if next_col >= 0 and next_col < num_cols:
                    next_row = row
                else:
                    continue
                # we move from the left part of the field to the right, or from right to the left;
                # so we should swap active and inactive constraints for the rows
                if (col == cols_in_left_part - 1 and move == +1) or (col == cols_in_left_part and move == -1):
                    next_active_rows_constr, next_inactive_rows_constr = next_inactive_rows_constr, next_active_rows_constr                 
            elif direction == 'vertical':
                next_row = row + move
                # next row is inside field
                if next_row >=0 and next_row < num_rows:
                    next_col = col
                else:
                    continue
            # extract values of constraints for the next col and next row
            next_col_value = cols_constr[next_col]
            next_row_value = next_active_rows_constr[next_row]
            # constraints allow to make the move
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

# number of cols in the left part of the field
cols_in_left_part = 8

#constraints for the cols of the field
cols_constr =[3,3,2,1,4,3,2,3,6,3,4,3,5,2,2,3]

#constraints for the rows in the left part of the field
left_rows_constr = [1,1,4,5,6,4]

#constraints for the rows in the right part of the field
right_rows_constr = [5,2,2,7,6,6]

# start cell
start = (0,0)

# finish cell
finish = (15,5)

def extract_message(field, path):
    """Function that extract message from the given field according to the given path.
       Input:
           field - tuple/list of tuples/lists of the same size, that consist of integers:
                  representation of the given field, where 0 denotes an empty cell;
           path - tuple of tuples of two integers: path from the corresponding field of the puzzle.
       Output:
           string - exctracted message: if path moved through a cell of the field and that cell is not empty,
           than the message will have a number from that cell in the corresponding place,
           otherwise there will be '-' character on that place."""
    num_rows = len(field)
    num_cols = len(field[0])
    message = ''
    # decremental loop for the number of rows
    for row in range(num_rows-1,-1,-1):
        for col in range(num_cols):
            cell_value = field[row][col]
            if (col,row) in path and cell_value > 0:
                message += str(cell_value)
            else:
                message += '-'
        # add newline character after each row
        message += '\n'
    return message

# bottom field from the puzzle, where 0 denotes an empty cell
bottom_field = ((0,0,8,6,0,8,0,0,0,0,0,0,0,2,0,9),
                (0,1,0,3,0,0,0,1,0,7,0,9,0,0,4,0),
                (7,0,4,0,6,0,9,0,5,4,0,3,4,0,1,0),
                (2,5,3,3,0,0,5,0,0,0,5,0,0,8,2,0),
                (0,0,5,0,0,5,0,0,0,5,0,0,6,3,0,0),
                (0,4,0,5,7,0,2,7,8,9,0,8,2,0,0,2))

if __name__ == '__main__':
    # find path in the upper field and extract and print corresponding message from the bottom field of the puzzle
    path = search(start, finish, cols_in_left_part, cols_constr, left_rows_constr, right_rows_constr)
    message = extract_message(bottom_field, path)
    print(message)
