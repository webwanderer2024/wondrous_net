import string

def solve_clocks(clocks_data,n):
    """Function, which exctracts messages from clocks for "Mr. Game & Watch" puzzle from MUMS Puzzle Hunt 2011:
    
       Puzzle - https://web.archive.org/web/20140401194553/http://www.ms.unimelb.edu.au/~mums/puzzlehunt/2011/puzzles/Act4.pdf
       Solution - https://web.archive.org/web/20140401194601/http://www.ms.unimelb.edu.au/~mums/puzzlehunt/2011/answers.html?puzzle=4.1
       
       English explanation - https://wondrousnet.blogspot.com/2024/01/solution-to-puzzle-mr-game-watch.html 
       Russian explanation - https://wondrousnet.blogspot.com/2024/01/mr-game-watch.html

       Input:
           clocks_data: list or tuple of tuples, each of which represents one corresponding clock; each tuple consists of four parts:
               1) integer from 0 to 11 - number of hours
               2) string - time of day, 'am' or 'pm'
               3) float - the angle between the minute hand and the hour hand
               4) boolean - it is about type of formula, used to compute the number of minutes:
                  if True, then a simpler formula is used: minutes = (2/11)*(30*hours + angle);
                  if False, then a little bit more complex formula is used: minutes = (2/11)*(30*hours + angle - 360).
           n - integer: number of exctracted messages.
       Returns:
           string of uppercase messages for corresponding time values separated by the new line symbol."""
    
    all_clocks_values = []
    # we collecting time values for clocks from bigger to smoller
    for clock in clocks_data:
        clock_values = []
        if clock[1] == 'am':
            hours = clock[0]
        elif clock[1] == 'pm':
            hours = 12 + clock[0]
        clock_values.append(hours)
        if clock[3]:
            minutes_value = (2/11)*(30*clock[0] + clock[2])
        else:
            minutes_value = (2/11)*(30*clock[0] + clock[2] - 360)
        current_value = minutes_value
        actual_time = int(minutes_value)
        clock_values.append(actual_time) # add value for minutes
        # compute and add smoller time values
        for i in range(n-2):
            current_value = (current_value - actual_time)*60
            actual_time = int(current_value)
            clock_values.append(actual_time)
        all_clocks_values.append(clock_values)
    all_messages = ''
    letters = string.ascii_uppercase
    # i is an index of the mesure of time, for which we want to construct the message
    for i in range(n): 
        # When we want to sort two clocks to construct message for some mesure of time,
        # we first need to compare their values for the previous mesure of time,
        # and if they are the same, we need to retain their order made by the previous sorting,
        # which is ensured by the Python sort() method. 
        if i > 0: # if i == 0, then clocks are already sorted
            all_clocks_values.sort(key = lambda clock_values: clock_values[i-1])
        message = ''
        for clock_values in all_clocks_values:
            value_for_letter = clock_values[i]
            letter = letters[value_for_letter - 1]
            message += letter
        all_messages += (message + '\n')
    return all_messages


#representation of clocks from puzzle
clocks_data = ((1,'am',69.47564,True),(0,'pm',29.35372,True),(4,'pm',-8.70545,True),(8,'am',-128.60642,True),
               (1,'am',-0.66474,True),(2,'am',-32.37728,True),(5,'am',-104.12833,True),(8,'pm',148.35595,False),
               (9,'am',-169.34332,True),(7,'pm',-160.02279,True),(5,'am',-98.75045,True),(3,'am',-82.73052,True),
               (0,'pm',71.59333,True),(3,'pm',-60.38542,True),(3,'am',20.48941,True),(11,'am',59.18092,False),
               (7,'pm',-137.11121,True),(1,'am',59.86097,True),(2,'pm',24.33518,True),(4,'am',-8.80010,True),
               (8,'pm',-134.47923,True),(8,'am',164.75629,False),(5,'am',-44.09744,True),(2,'pm',40.46877,True))


if __name__ == '__main__':
    messages = solve_clocks(clocks_data,5) # command to extract all messages from clocks in puzzle
    print(messages)
