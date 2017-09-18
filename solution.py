assignments = []

# Setting to define if Sudoku to solve is diagonal or not. Set to False if not.
DIAGONAL = True


def cross(a, b):
    """Cross product of elements in A and elements in B."""
    return [s + t for s in a for t in b]

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonal_units = [[r + c for r, c in zip(rows, cols)], [r + c for r, c in zip(rows, cols[::-1])]]


unitlist = row_units + column_units + square_units

if DIAGONAL:
    unitlist = unitlist + diagonal_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], []))-set([s])) for s in boxes)


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
        second_dual_boxes = [second_box for second_box in dual_boxes
                             if dual_box != second_box and values[dual_box] == values[second_box]
                             and second_box in peers[dual_box]]

        for second_dual_box in second_dual_boxes:
            boxes_to_clean = [peer_set for peer_set in unitlist
                              if (dual_box in peer_set and second_dual_box in peer_set)]
            for group in boxes_to_clean:
                for box in group:
                    # weed out boxes with empty values or solved boxes
                    if len(values[box]) > 1 and box != dual_box and box != second_dual_box:
                        for digit in values[dual_box]:
                            assign_value(values, box, values[box].replace(digit, ''))
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
        return
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    return


def eliminate(values):
    """
    Eliminate values from peers of each box with a single value.
    Args:
        a sudoku in dictionary form
    Returns:
        the values dictionary with eliminated values from peers.
    """

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit, ''))

    return values


def only_choice(values):
    """
    Finalize all values that are the only choice for a unit.
    Args:
        a sudoku in dictionary form
    Returns:
        resulting Sudoku in dictionary form after filling in only choices.
    """

    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)

    return values


def reduce_puzzle(values):
    """
    Executes eliminate, only_choice and naked_twins functions until no further reduction possible.
    Args:
        a sudoku in dictionary form
    Returns:
        resulting Sudoku in dictionary form after reduction.
    """

    stalled = False
    while not stalled:
        solved_values_before = len(
            [box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len(
            [box for box in values.keys() if len(values[box]) == 1])
        # Stop if no further changes were made
        stalled = solved_values_before == solved_values_after
        # Stop if unsolvable (a box has zero available values)
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values


def search(values):
    """
     Recursive call of reduce_puzzle and DFS trial and error.
     Args:
         a sudoku in dictionary form
     Returns:
         resulting Sudoku in dictionary form. "False" if no solution could be found
     """

    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


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

    values = grid_values(grid)
    values = search(values)

    return values


if __name__ == '__main__':
    # diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    # diag_sudoku_grid = '...95.7..7513.2...2.4.18536.......93.2.....1.84.......96253.1.4...2.9367..7.41...'
    # diag_sudoku_grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. ' +
              'Not a problem! It is not a requirement.')
