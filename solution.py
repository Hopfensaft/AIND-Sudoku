assignments = []


def cross(a, b):
    """Cross product of elements in A and elements in B."""
    return [s + t for s in a for t in b]


rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)

values = {"A1": "", "A2": "", "A3": "", "A4": "", "A5": "", "A6": "", "A7": "", "A8": "", "A9": "",
          "B1": "", "B2": "", "B3": "", "B4": "", "B5": "", "B6": "", "B7": "", "B8": "", "B9": "",
          "C1": "", "C2": "", "C3": "", "C4": "", "C5": "", "C6": "", "C7": "", "C8": "", "C9": "",
          "D1": "", "D2": "", "D3": "", "D4": "", "D5": "", "D6": "", "D7": "", "D8": "", "D9": "",
          "E1": "", "E2": "", "E3": "", "E4": "", "E5": "", "E6": "", "E7": "", "E8": "", "E9": "",
          "F1": "", "F2": "", "F3": "", "F4": "", "F5": "", "F6": "", "F7": "", "F8": "", "F9": "",
          "G1": "", "G2": "", "G3": "", "G4": "", "G5": "", "G6": "", "G7": "", "G8": "", "G9": "",
          "H1": "", "H2": "", "H3": "", "H4": "", "H5": "", "H6": "", "H7": "", "H8": "", "H9": "",
          "I1": "", "I2": "", "I3": "", "I4": "", "I5": "", "I6": "", "I7": "", "I8": "", "I9": ""}

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    dual_boxes = [box for box in values.keys() if len(values[box]) == 2]
    for dual_box in dual_boxes:
        dual_boxes.remove(dual_box)
        second_dual_boxes = [second_box for second_box in dual_boxes
                           if values[dual_box] == values[second_box]]

        for second_dual_box in second_dual_boxes:
            boxes_to_clean = []

            if dual_box[0] == second_dual_box[0]:
                boxes_to_clean = [box for box in values.keys()
                                  if box[0] == dual_box[0] and not (box == second_dual_box or box == dual_box)]

            if dual_box[1] == second_dual_box[1]:
                boxes_to_clean = boxes_to_clean + [box for box in values.keys()
                                                   if box[1] == dual_box[1] and not (box == second_dual_box or box == dual_box)]

            for box in boxes_to_clean:
                assign_value(values, box, values[box].replace(values[dual_box][1], ''))
                assign_value(values, box, values[box].replace(values[dual_box][0], ''))
                print("Tried naked twin")

    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value,
                    then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    if values is False:
        print("unable to solve")
        return
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit,''))

    return values


def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values


def reduce_puzzle(values):
    # solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len(
            [box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len(
            [box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        return search(new_sudoku)


def init_grid(grid):
    initialize_values = grid_values(grid)

    for val in initialize_values:
        assign_value(values, val, initialize_values[val])

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid.
        False if no solution exists.
    """
    init_grid(grid)

    search(values)

    if values == False:
        print("unsolvable!")
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    # diag_sudoku_grid = '...95.7..7513.2...2.4.18536.......93.2.....1.84.......96253.1.4...2.9367..7.41...'
    # diag_sudoku_grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. ' +
              'Not a problem! It is not a requirement.')
