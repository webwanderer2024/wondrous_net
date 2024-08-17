import string

def generate_maze(num_cols, num_rows, imaginary_cells,
                  cells_on_the_left_edge, cells_on_the_right_edge, cells_with_right_border_inside_maze,
                  cells_with_right_gate_by_colours, cells_with_upper_gate_by_colours):
    """Function for creating representation of the maze for the puzzle Cat Walk from MUMS Puzzle Hunt 2012 competition.
       English - https://wondrousnet.blogspot.com/2024/03/solution-to-puzzle-cat-walk.html
       Russian - https://wondrousnet.blogspot.com/2024/03/cat-walk.html
       Input:
           num_cols - integer, number of columns in the maze;
           num_rows - integer, number of rows in the maze;
           imaginary_cells - list or tuple of tuples of two integers, each of which represent one cell,
               that is inside rectangular grid of num_cols*num_rows, but not a part of the maze;
           cells_on_the_left_edge - tuple of tuples of two integers, each of which represent one cell on the left edge of the maze;
           cells_on_the_right_edge - tuple of tuples of two integers, each of which represent one cell on the right edge of the maze;
           cells_with_right_border_inside_maze - list or tuple of tuples of two integers, each of which represnt one cell, that has a right border with another cell;
           cells_with_right_gate_by_colours - dictionary, where keys are strings, that correspond to the colours of the gates between cells,
               and values are lists or tuples of tuples of two integers, each of which represent one cell, that has a right gate of the colour of the key;
           cells_with_upper_gate_by_colours - dictionary, where keys are strings, that correspond to the colours of the gates between cells,
               and values are lists or tuples of tuples of two integers, each of which represent one cell, that has an upper gate of the colour of the key.
       Output:
           dictionary represented the maze: it's keys are tuples of two integers, represented cells;
           it's values are dictionaries, where keys are strings of available movements ('up', 'down', 'left' or 'right')
           and values are colours of the gates associated with that movements (strings represented colours or None)."""
    cells_with_left_border = cells_on_the_left_edge
    cells_with_right_border = cells_on_the_right_edge
    for cell in cells_with_right_border_inside_maze:
        # extend the tuple of cells with right border
        cells_with_right_border += (cell,)
        # extend the tuple of cells with left border
        cells_with_left_border += ((cell[0]+1,cell[1]),)        
    cells_with_right_gate = {}
    cells_with_left_gate = {}
    for colour in cells_with_right_gate_by_colours:
        for cell in cells_with_right_gate_by_colours[colour]:
            cells_with_right_gate[cell] = colour
            cells_with_left_gate[(cell[0]+1,cell[1])] = colour
    cells_with_upper_gate = {}
    cells_with_lower_gate = {}
    for colour in cells_with_upper_gate_by_colours:
        for cell in cells_with_upper_gate_by_colours[colour]:
            cells_with_upper_gate[cell] = colour
            cells_with_lower_gate[(cell[0],cell[1]+1)] = colour                                 
    maze = {}
    # create a maze, row by row
    for row in range(num_rows):
        # create one row
        for col in range(num_cols):
            cell = (col,row)
            if cell not in imaginary_cells:
                cell_gates = {}
                # vertical gates
                if cell in cells_with_upper_gate:
                    cell_gates['up'] = cells_with_upper_gate[cell]
                if cell in cells_with_lower_gate:
                    cell_gates['down'] = cells_with_lower_gate[cell]
                # horizontal gates    
                if cell in cells_with_right_gate:
                    cell_gates['right'] = cells_with_right_gate[cell]
                elif cell not in cells_with_right_border:
                    cell_gates['right'] = None
                if cell in cells_with_left_gate:
                    cell_gates['left'] = cells_with_left_gate[cell]
                elif cell not in cells_with_left_border:
                    cell_gates['left'] = None                    
                maze[cell] = cell_gates
    return maze

def search(maze, start_cells, goal_cells, palette, first_colour):
    """Function that perform depth-first search in the maze from the multiple start cells to the goal cells
       according to the colours in palette and first colour.
       Input:
           maze - dictionary represented the maze: it's keys are tuples of two integers, represented cells;
               it's values are dictionaries, where keys are strings of available movements ('up', 'down', 'left' or 'right')
               and values are colours of the gates associated with that movements (strings represented colours or None);
           start_cells - list or tuple of tuples of two integers, collection of the starting cells;
           goal_cells - list or tuple of tuples of two integers, collection of the goal cells;
           palette - dictionary, consisted of strings, where keys are colours for the path and values are corresponding next colours;
           first_colour - string, colour of the first coloured gate from palette.
       Output:
           if some search is successful - return phrase corresponding to that search;
           if all searches are failed - return False."""
    for cell in start_cells:
        phrase = depth_first_search(maze, cell, goal_cells,(), first_colour, palette, '')
        if phrase:
            return phrase
    return False

def depth_first_search(maze, current_cell, goal_cells, path, current_colour, palette, current_phrase):
    """Function that performs search in depth-first fashion in the maze from the current_cell to the goal_cells
       according to the current_colour of the gate and following colours of the gates in palette.
       Input:
           maze - dictionary represented the maze: it's keys are tuples of two integers, represented cells;
               it's values are dictionaries, where keys are strings of available movements ('up', 'down', 'left' or 'right')
               and values are colours of the gates associated with that movements (strings represented colours or None);
           current_cell - tuple of two integers, current cell of search;
           goal_cells - list or tuple of tuples of two integers, collection of the goal cells;
           path - tuple of tuples of two integers: all cells on the path made so far;
           current_colour - string, colour of the next coloured gate on the path;
           palette - dictionary, consisted of strings, where keys are colours for the path and values are corresponding next colours;
           current_phrase - string, it's a phrase, generated  so far.
       Output:
           if search is successful, function will return string, that is a generated phrase;
           otherwise it will return False."""
    path += (current_cell,)
    if current_cell in goal_cells:
        return current_phrase
    else:
        near_cells_with_letters_and_colours = get_near_cells_with_letters_and_colours(maze, current_cell, current_colour, palette)
        for (cell, letter, colour) in near_cells_with_letters_and_colours:
            # required path is acyclic
            if cell not in path:
                extended_phrase = current_phrase + letter
                phrase = depth_first_search(maze, cell, goal_cells, path, colour, palette, extended_phrase)
                if phrase != False:
                    return(phrase)
    return False
                    
def get_near_cells_with_letters_and_colours(maze, cell, colour, palette):
    """Function that for the current cell and current colour will find available near cells,
       and also letters of the message and next colours, associated with passage to that cells.
       Input:
           maze - dictionary represented the maze: it's keys are tuples of two integers, represented cells;
               it's values are dictionaries, where keys are strings of available movements ('up', 'down', 'left' or 'right')
               and values are colours of the gates associated with that movements (strings represented colours or None);
           cell - tuple of two integers, current cell;
           colour - string, represented colour of the next coloured gate;
           palette - dictionary, consisted of strings, where keys are colours for the path and values are corresponding next colours;
       Output:
           tuple of tuples, each of which consists of three parts:
           1) tuple of two integers - one of the near cells;
           2) string: if movement to that cell passes through vertical coloured gate, than this string will be one upper-case letter,
              that correspond to the column-number of that cell; otherwise it will be empty string;
           3) string - following colour of the gate."""
    col = cell[0]
    row = cell[1]
    near_cells_with_letters_and_colours = ()
    for direction in maze[cell]:
        gate_colour = maze[cell][direction]
        # gate has the same colour
        if gate_colour == colour:
            # find next colour from the palette
            next_colour = palette[colour]
            if direction == 'up' or direction == 'down':
                letter = string.ascii_uppercase[col]
            elif direction == 'left' or direction == 'right':
                letter = ''
        # gate has no colour
        elif gate_colour == None:
            # next colour will be the same
            next_colour = colour
            letter = ''
        # gate has a different colour
        else:
            continue        
        if direction == 'up':
            near_cell = (col, row+1)
        elif direction == 'down':
            near_cell = (col,row-1)
        elif direction == 'left':
            near_cell = (col-1,row)
        elif direction == 'right':
            near_cell = (col+1,row)            
        near_cells_with_letters_and_colours += ((near_cell, letter, next_colour),)        
    return near_cells_with_letters_and_colours

# number of columns in the maze
num_cols = 26
# number of rows in the maze;
# actually, the maze in the puzzle contains 20 rows, but for search in it one more row is added on the top,
# that contains real cells after exits from the maze and imaginary cells in all other positions
num_rows = 21

# cells inside rectangular grid that are not part of the maze
imaginary_cells = ((0,20),(1,20),(2,20),(3,20),
                   (5,20),(6,20),
                   (8,20),(9,20),(10,20),
                   (12,20),(13,20),(14,20),(15,20),(16,20),
                   (18,20),
                   (20,20),
                   (22,20),(23,20),
                   (25,20))

# cells on the left edge of the maze
cells_on_the_left_edge = ((0,0),
                          (0,1),
                          (0,2),
                          (0,3),
                          (0,4),
                          (0,5),
                          (0,6),
                          (0,7),
                          (0,8),
                          (0,9),
                          (0,10),
                          (0,11),
                          (0,12),
                          (0,13),
                          (0,14),
                          (0,15),
                          (0,16),
                          (0,17),
                          (0,18),
                          (0,19),
                          (4,20),(7,20),(11,20),(17,20),(19,20),(21,20),(24,20))

# cells on the right edge of the maze
cells_on_the_right_edge = ((25,0),
                           (25,1),
                           (25,2),
                           (25,3),
                           (25,4),
                           (25,5),
                           (25,6),
                           (25,7),
                           (25,8),
                           (25,9),
                           (25,10),
                           (25,11),
                           (25,12),
                           (25,13),
                           (25,14),
                           (25,15),
                           (25,16),
                           (25,17),
                           (25,18),
                           (25,19),
                           (4,20),(7,20),(11,20),(17,20),(19,20),(21,20),(24,20))

# cells that have a border with another cell on the right side                  
cells_with_right_border_inside_maze = ((12,0),
                                       (13,2),
                                       (9,3),(18,3),
                                       (14,4),(22,4),
                                       (20,6),
                                       (16,10),
                                       (20,12),
                                       (17,13),
                                       (7,14),
                                       (15,17),
                                       (19,18),
                                       (5,19),(19,19))

# cells with coloured gate on the right side
cells_with_right_gate_by_colours = {'blue':((2,1),(21,1),
                                            (4,5),
                                            (21,15)),
                                    'red':((1,2),
                                           (1,6),
                                           (4,8),
                                           (12,9),
                                           (4,11),(15,11),
                                           (15,15),
                                           (7,16)),
                                    'green':((21,9),
                                             (2,10),
                                             (1,12),
                                             (20,14),
                                             (3,15),
                                             (17,16),
                                             (21,17)),
                                    'gray':((9,13),)}

# cells with coloured gate on the upper side
cells_with_upper_gate_by_colours = {'blue':((0,0),(24,0),
                                            (15,1),
                                            (0,2),(23,2),
                                            (8,3),
                                            (14,5),(21,5),
                                            (13,6),
                                            (3,8),(9,8),(22,8),
                                            (2,9),(7,9),(17,9),
                                            (0,11),(19,11),
                                            (18,12),
                                            (5,13),(8,13),
                                            (0,14),(10,14),
                                            (6,15),(19,15),(25,15),
                                            (5,16),(16,16),(19,16),
                                            (11,17),(18,17),(24,17),
                                            (8,18),(25,18),
                                            (4,19),(19,19),(21,19)),
                                    'red':((1,0),(12,0),
                                           (20,1),
                                           (7,2),
                                           (10,4),(23,4),
                                           (1,7),
                                           (18,8),
                                           (11,10),
                                           (8,11),
                                           (14,12),
                                           (2,13),(13,13),(19,13),
                                           (24,14),
                                           (3,15),(20,15),
                                           (20,16),
                                           (4,17),(20,17),
                                           (14,18),(23,18),
                                           (17,19),(24,19)),
                                    'green':((6,0),(19,0),
                                             (1,1),(11,1),(25,1),
                                             (18,2),
                                             (2,3),(25,3),
                                             (14,4),
                                             (0,5),(24,5),
                                             (7,6),(22,6),
                                             (3,7),(14,7),
                                             (1,9),
                                             (8,10),(20,10),
                                             (4,12),
                                             (1,14),(18,14),
                                             (1,15),(4,15),(21,15),
                                             (21,16),(23,16),
                                             (14,17),
                                             (2,18),(20,18),
                                             (11,19)),
                                    'gray':((17,0),(23,0),
                                            (4,1),(24,1),
                                            (3,2),(14,2),(19,2),
                                            (1,3),(15,3),(20,3),(24,3),
                                            (4,4),(11,4),
                                            (1,5),(20,5),(25,5),
                                            (4,6),
                                            (0,7),(19,7),
                                            (7,8),(14,8),(24,8),
                                            (0,9),(4,9),(18,9),
                                            (2,10),(13,10),(24,10),
                                            (1,11),(6,11),(22,11),
                                            (17,12),(23,12),
                                            (4,13),(11,13),(21,13),
                                            (2,14),(4,14),(21,14),
                                            (0,15),(13,15),(18,15),
                                            (15,16),(17,16),(24,16),
                                            (0,17),(21,17),
                                            (4,18),(19,18),(22,18),
                                            (7,19))}

# starting cells
start_cells = ((12,0),(13,0))
# goal cells
goal_cells = ((4,20),(7,20),(11,20),(17,20),(19,20),(21,20),(24,20))

# colours of gates for the first message
gray_palette = {'gray':'gray'}
# colours of gates for the second message
rbg_palette = {'red':'blue','blue':'green','green':'red'}

if __name__ == '__main__':
    # generate the maze in the puzzle
    maze = generate_maze(num_cols, num_rows, imaginary_cells,
                         cells_on_the_left_edge, cells_on_the_right_edge, cells_with_right_border_inside_maze, 
                         cells_with_right_gate_by_colours, cells_with_upper_gate_by_colours)
    # command to exctract the first message in the puzzle
    phrase = search(maze,start_cells,goal_cells, gray_palette,'gray')
    print(phrase)
    # command to extract the second message in the puzzle
    phrase = search(maze,start_cells,goal_cells, rbg_palette,'red')
    print(phrase)
