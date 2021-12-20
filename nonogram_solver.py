#! /usr/bin/python3

"""
    This program will solve nonogram puzzles for any x*x size with given starting conditions.
"""

def find_options(length, filled, pattern='', empty=''):
    """ This function finds all possibilities for the starting condition of the rows or columns. """

    total_empty = length - sum(filled)
    extra = total_empty - len(filled) + 1
    lines = []
    ones = filled[0]

    for pad in range(0, extra + 1):
        # Loop over each possible set of padding.

        line = ''
        blanks = len(filled)
        total_blanks = total_empty - pad

        # Set the first value of the sub-string.
        line += '0' * pad
        line += '1' * ones

        # Subtract from the number of dividers left.
        blanks -= 1

        if blanks > 0:
            # If there are still dividers, leave a blank for it.
            line += '0'

            # Subtract this divider from the total blanks left.
            total_blanks -= 1

        if len(filled) > 1:
            # If the string has not been fully built yet, then generate the next sub-string.
            subs = find_options(length - len(line), filled[1:])

            for sub in subs:
                # Append this section with the sub-sections found in the recursion.
                lines.append(line + sub)
        else:
            # There are no parts left so pad with the remaining blanks.
            line += '0' * total_blanks

            # Add the string to the possible values.
            lines.append(line)

    if len(lines[0]) == length and pattern != '':
        temp_lines = []

        mask = int(pattern, base=2)

        for line in lines:
            if (int(line, base=2) & mask) == mask:
                temp_lines.append(line)

            lines = temp_lines

    if len(lines[0]) == length and empty != '':
        temp_lines = []

        mask = int(empty, base=2)

        for line in lines:
            if not int(line, base=2) & mask:
                temp_lines.append(line)

            lines = temp_lines

    # Return the possible values.
    return lines

def find_overlap(length, patterns):
    """ This function finds the overlap between the current possibilities for a row or column. """

    # Set the initial maks to everything set.  This handles up to a 32x32 grid.
    overlap = 0xFFFFFFFF

    for pattern in patterns:
        # Convert each possibility to an integer based on the string bit pattern and generate
        # the overlap mask.
        overlap &= int(pattern, base=2)

    # Return the value as a bit pattern string.
    return "{0:b}".format(overlap).zfill(length)

def compare_existing(length, patterns, existing=''):
    """
        This function adds information from a partially user-solved row or column to the
        computer-generated row or column.
    """

    if existing == '':
        # Set the default to a completely unset bit pattern string.
        existing = '0' * length

    # Lookup the overlap value.
    pattern = int(find_overlap(length, patterns), base=2)

    # Merge the overlap value and the already existing value.
    pattern |= int(existing, base=2)

    # Return the value as a bit pattern string.
    return "{0:b}".format(pattern).zfill(length)

def update_existing(col_existing, row_existing):
    """
        This function updates the rows based on the columns and vice-versa.  It basically rotates
        one matrix in memory and compares it to the other one.
    """

    for row_index in range(0, len(col_existing)):
        for col_index in range(0, len(row_existing)):
            if col_existing[row_index][col_index] == '1':
                row_existing[col_index] \
                    = row_existing[col_index][:row_index] \
                    + '1' \
                    + row_existing[col_index][row_index+1:]

            if row_existing[row_index][col_index] == '1':
                col_existing[col_index] \
                    = col_existing[col_index][:row_index] \
                    + '1' \
                    + col_existing[col_index][row_index+1:]

    return row_existing, col_existing

def solve(length, horizontal_grid, vertical_grid):
    """
        This function will solve a nonogram given the length, horizontal_grid, and vertical_grid.
    """

    horizontal_existing = []
    vertical_existing = []

    horizontal_backup = []
    vertical_backup = []

    horizontal_empty = []
    vertical_empty = []

    for row in horizontal_grid:
        # Find the initial patterns for each row.
        patterns = find_options(length, row)

        horizontal_existing.append(find_overlap(length, patterns))
        horizontal_empty.append(find_empty_2(length, patterns))

    for col in vertical_grid:
        # Find the initial patterns for each column.
        patterns = find_options(length, col)

        vertical_existing.append(find_overlap(length, patterns))
        vertical_empty.append(find_empty_2(length, patterns))

    passes = 0
    done = 0

    while not done:
        # If changes were made to the grid, keep trying to solve the puzzle.

        # Set the backed-up data to the current data.
        horizontal_backup = horizontal_existing[:]
        vertical_backup = vertical_existing[:]

        vertical_existing, horizontal_existing \
            = update_existing(horizontal_existing, vertical_existing)

        vertical_empty, horizontal_empty \
            = update_existing(horizontal_empty, vertical_empty)

        for index in range(0, len(horizontal_grid)):
            # Find the current patterns for each row.
            patterns = find_options(
                length,
                horizontal_grid[index],
                horizontal_existing[index],
                horizontal_empty[index]
            )

            # Update the horizontal positions.
            horizontal_existing[index] = find_overlap(length, patterns)

            # Find the empty positions for the available patterns.
            horizontal_empty[index] = find_empty_2(length, patterns)

        for index in range(0, len(vertical_grid)):
            # Find the current patterns for each column.
            patterns = find_options(
                length,
                vertical_grid[index],
                vertical_existing[index],
                vertical_empty[index]
            )

            # Update the vertical positions.
            vertical_existing[index] = find_overlap(length, patterns)

            # Find the empty positions for the available patterns.
            vertical_empty[index] = find_empty_2(length, patterns)

        if (horizontal_existing == horizontal_backup and vertical_existing == vertical_backup):
            done = 1

        passes += 1

    print("Passes: %u\n\n" % passes)

    return horizontal_existing, horizontal_empty

def find_empty_2(length, potential):
    """ This function finds the empty positions based of the potential fill positions. """

    patterns = potential[:]

    for index, pattern in enumerate(patterns):
        # Flip the bits of each position.
        patterns[index] = ''.join('1' if bit == '0' else '0' for bit in pattern)

    # Find the overlap of the empty positions.
    empty = find_overlap(length, patterns)

    return empty


LENGTH = 15

HORIZONTAL_GRID = [
    [3, 2],
    [1, 4, 1],
    [2],
    [1, 2],
    [1, 5],
    [2, 7],
    [11],
    [5, 2],
    [4, 5],
    [3, 2, 1],
    [3, 1, 3],
    [2, 3, 3],
    [2, 3, 3],
    [1, 2, 2, 2],
    [5, 4]
]

VERTICAL_GRID = [
    [2, 2],
    [1, 1, 3],
    [2, 2, 5, 1],
    [1, 1, 9],
    [1, 5, 3, 1],
    [1, 5, 1],
    [1, 5, 2],
    [3, 2, 3],
    [2, 2],
    [2, 6],
    [2, 2, 2],
    [1, 1, 1],
    [3, 5],
    [2, 4],
    [5]
]

def main():
    """ This is the main function of the program. """

    solved, empty = solve(LENGTH, HORIZONTAL_GRID, VERTICAL_GRID)

    print("SOLVED:\t\tEMPTY:")

    for index in range(LENGTH):
        print(f"{solved[index]}\t{empty[index]}")

if __name__ == "__main__":
    main()

# TODO: This may be able to be simplified with numpy.
