def solve_grids(grids, strips, outlines_per_row):
    """Function for solving grids for puzzle Black and White from MUMS Puzzle Hunt 2010 competition.
       English - https://wondrousnet.blogspot.com/2024/09/solution-to-puzzle-black-and-white.html
       Russian - https://wondrousnet.blogspot.com/2024/09/black-and-white.html
       Input:
           grids - tuple of tuples of strings, where each tuple represent one grid, and each string represent one row of that grid;
           each symbol of a string denote colour of the corresponding cell of the grid ('w' for white and 'b' for black).
           strips - tuple of strings, where each string represent one strip;
           each symbol of a string denote colour of the corresponding cell of the strip ('w' for white and 'b' for black).
           outlines_per_row - integer: amount of outlines of placings in one row of output.
       Output:
           If all grids are solved, then the function will return string of outlines of all placings,
           consisted of bars, underscores and spaces, with outlines_per_row outlines in one row;
           otherwise function will return False."""
    first_grid = grids[0]
    num_rows = len(first_grid)
    num_cols = len(first_grid[0])
    # sorting strips according to length in decreasing order to make the problem easier
    strips = tuple(sorted(strips,key = len,reverse = True))
    outlines = ()
    for grid_values in grids:
        # represent the grid as a dictionary for search
        grid = {}
        for row in range(num_rows):
            for col in range(num_cols):
                grid[(col,row)] = grid_values[row][col]
        # try to find placing with depth-first search
        placing = depth_first_search(grid, num_cols, num_rows, strips,(), ())
        if placing:
            # form outline of a placing
            outline = get_placing_outline(placing, num_cols, num_rows)
            outlines += (outline,)
        else:
            return False
    # combine outlines
    output = get_output(outlines, outlines_per_row)
    return output
        
def depth_first_search(grid, num_cols, num_rows, strips, occupied_cells, placing):
    """Function that perform depth-first search to place the strips on the grid.
       Input:
           grid - dictionary, where keys are tuples of two integers representing cells,
           and values are strings of one symbol that denote colour of that cell ('w' for white and 'b' for black).
           num_cols - integer: number of columns in the grid.
           num_rows - integer: number of rows in the grid.
           strips - tuple of strings, where each string represent one strip;
           each symbol of a string denote colour of the corresponding cell of the strip ('w' for white and 'b' for black).
           occupied_cells - tuple of tuples of two integers, where each tuple represent one cell that is under strip already.
           placing - tuple of tuples, each of which represnt one placed strip and consist of 3 parts:
           1) tuple of two integers that represent position of left lower cell of the strip;
           2) string: orientation of the strip ('horizontal' or 'vertical');
           3) integer: length of the strip.
       Output:
           If search is successful, the function will return corresponding final placing;
           otherwise the function will return False."""
    if strips == ():
        # all strips are placed
        return placing
    else:
        # current strip of search
        current_strip = strips[0]
        # strips for further search
        next_strips = strips[1:]
        # position is used for search, representation is used for answer
        for (position,representation) in get_strip_positions(current_strip, num_cols, num_rows):
            position_is_possible = True
            # check that position is possible
            for cell in position:
                if position[cell] != grid[cell] or cell in occupied_cells:
                    position_is_possible = False
                    break
            if position_is_possible:
                next_occupied_cells = occupied_cells                        
                for cell in position:
                    next_occupied_cells += (cell,)
                next_placing = placing + (representation,)
                final_placing = depth_first_search(grid, num_cols, num_rows, next_strips, next_occupied_cells, next_placing)
                if final_placing:
                    return final_placing
    return False

def get_strip_positions(strip, num_cols, num_rows):
    """Function that generate possible positions for the given strip according to the number of columns and rows in the grid.
       Input:
           strip - string that represent one strip, where each symbol denote colour of the corresponding cell ('w' for white and 'b' for black).
           num_cols - integer: number of columns in the grid.
           num_rows - integer: number of rows in the grid.
       Output:
           generator that will generate potential positions of the strip on the grid with its representation as tuples of two elements:
           1) dictionary, where keys are tuples of two integers that represent cells of the grid,
              and values are strings of one symbol, that denote colours of the cells of the strip ('w' for white and 'b' for black);
           2) tuple of tuples, each of which represnt one placed strip and consist of 3 parts:
              1) tuple of two integers that represent position of left lower cell of the strip;
              2) string: orientation of the strip ('horizontal' or 'vertical');
              3) integer: length of the strip."""
    strip_len = len(strip)
    # we should also consider reversed strip, if it is different from the original one
    reversed_strip = strip[::-1]
    if strip == reversed_strip:
        patterns = (strip,)
    else:
        patterns = (strip, reversed_strip)
    # generate horizontal placings of the strip 
    for row in range(num_rows):
        for col in range(num_cols - strip_len + 1):
            for pattern in patterns:
                position = {}
                current_col = col
                for colour in pattern:
                    position[(current_col, row)] = colour
                    current_col += 1
                yield (position, ((col,row),'horizontal',strip_len))
    # generate vertical placings of the strip 
    for col in range(num_cols):
        for row in range(num_rows - strip_len + 1):
            for pattern in patterns:
                position = {}
                current_row = row
                for colour in pattern:
                    position[(col, current_row)] = colour
                    current_row += 1
                yield (position, ((col,row),'vertical',strip_len))
            
def get_placing_outline(placing, num_cols, num_rows):
    """Function that creates outline of the placing for output that consists of bars, underscores and spaces.
       Input:
           placing - tuple of tuples, each of which represnt one placed strip and consist of 3 parts:
           1) tuple of two integers that represent position of left lower cell of the strip;
           2) string: orientation of the strip ('horizontal' or 'vertical');
           3) integer: length of the strip.
           num_cols - integer: number of columns in the grid.
           num_rows - integer: number of rows in the grid.
       Output:
           list of strings, where each string, consisted of bars, underscores and spaces, represent one horizontal level of the outline."""
    cells_without_left_border = ()
    cells_without_lower_border = ()
    for strip in placing:
        first_cell = strip[0]
        col,row = first_cell[0],first_cell[1]
        orientation = strip[1]
        strip_len = strip[2]
        if orientation == 'horizontal':
            for strip_index in range(1, strip_len):
                cells_without_left_border += ((col + strip_index, row),)
        elif orientation == 'vertical':
            for strip_index in range(1, strip_len):
                cells_without_lower_border += ((col, row + strip_index),)
    outline = []
    # decremental loop for rows with one additional row for the upper border of the grid
    for row in range(num_rows,-1,-1):
        level = ''
        # loop for cols with one additional col for the right border of the grid
        for col in range(num_cols+1):
            cell = (col,row)
            if row < num_rows and (col == 0 or col == num_cols or not cell in cells_without_left_border):
                level += '|'
            else:
                level += ' '
            if col < num_cols:
                if row == 0 or row == num_rows or not cell in cells_without_lower_border:
                    level += '_'
                else:
                    level += ' '
        outline.append(level)
    return outline

def get_output(outlines, outlines_per_row):
    """Function that combines outlines to create output with outlines_per_row outlines in one row.
       Input:
           outlines - tuple of lists of strings, where each of the lists represent outline of one placing;
           each string represent one horizontal level of the outline and consists of bars, underscores and spaces.
           outlines_per_row - integer: amount of outlines in one row of output.
       Output:
           string, where outlines of the placings arranged in outlines_per_row outlines in one row with one space between them,
           and there is a new line after each horizontal level of one row and between different rows."""
    outlines_len = len(outlines)
    output = ''
    # determine starting index for every row
    for first_index in range(0, outlines_len, outlines_per_row):
        last_index = min(first_index + outlines_per_row, outlines_len)
        # add first outline to the row
        one_row = outlines[first_index]
        # add other outlines to the row
        for current_outline in outlines[first_index+1:last_index]:
            level_index = 0
            for level in current_outline:
                one_row[level_index] += ' ' + level
                level_index += 1
        for level in one_row:
            output += level + '\n'
    return output

# strips for the puzzle            
strips = ('ww','wb','bb','www','wwb','wbw','wbb','bwb','bbb')

# grids for the puzzle
grid01 = ('bwbww','bwbbb','wbwbw','bwwbw','bwwbb')
grid02 = ('bwbwb','bwbwb','wbwbw','wwbbb','wbbww')
grid03 = ('wwwbw','bbwww','bbbww','wwbbw','bbwbb')
grid04 = ('wwbbw','wbwbb','bwwwb','wwbbw','bbbwb')
grid05 = ('wwwwb','bbbbw','bbwbb','bwwbb','wwwwb')
grid06 = ('wbwwb','bwwbw','bbbbb','wwwbw','bwbww')
grid07 = ('wbwww','wwbbw','wbbbw','bbbbw','wbbww')
grid08 = ('wbbww','wwwbb','bwbww','bwbwb','bbwwb')
grid09 = ('bbbww','wwbww','wbbww','bwwwb','bbwbb')
grid10 = ('wwbbb','wbbbb','wbbwb','bwbww','bwwww')
grid11 = ('wwwww','bbbbb','wwbbw','wwbbb','bbbww')
grid12 = ('bbbbb','wwbwb','wwwwb','wwbwb','wwbwb')
grid13 = ('bwbwb','wwwbb','bwbwb','bwbbw','wwbwb')
grid14 = ('wbwwb','wbwbb','wwbbb','wwbbb','wwbbw')
grid15 = ('wwbbw','wwbww','bbbww','bbbww','bbwbw')
grid16 = ('wbwbw','wbwww','bbbbb','bwwww','bwbwb')
grid17 = ('wwwwb','wwwww','bbbbw','bbbwb','bwbbb')
grid18 = ('wbbww','bwwbb','bwwwb','bbbwb','wbwwb')
grid19 = ('bwwbw','wbwww','bwbwb','bwwbw','bbbbw')
grid20 = ('wbbwb','bbwbw','wwwwb','wbbbb','wwbwb')
grid21 = ('bbbwb','bbwbw','wbbww','bbwwb','wwbww')
grid22 = ('wwbbw','wbbbw','bwwwb','bwbbb','bwbww')
grid23 = ('wbwww','wwbwb','bbwww','wbwbb','bbbwb')
grid24 = ('bwwbb','wwwww','bwwww','bbbbb','wwbbb')
grid25 = ('wwwww','bbbww','bbbbw','bwbww','wwbbb')

# given grids together as a tuple
grids = (grid01,grid02,grid03,grid04,grid05,
         grid06,grid07,grid08,grid09,grid10,
         grid11,grid12,grid13,grid14,grid15,
         grid16,grid17,grid18,grid19,grid20,
         grid21,grid22,grid23,grid24,grid25)

# final grid for the puzzle
final_grid = ('bwwww','bbwbb','bbbww','wbwbb','wwbbw')

# number of outlines of placings in one row for the output
outlines_per_row = 5

if __name__ == '__main__':
    # solve the given grids for the puzzle
    answer = solve_grids(grids, strips, outlines_per_row)
    print(answer)
    # solve the final grid for the puzzle
    answer = solve_grids((final_grid,), strips, outlines_per_row)
    print(answer)
