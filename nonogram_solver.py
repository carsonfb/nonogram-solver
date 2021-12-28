#! /usr/bin/python3

"""
    This program will solve nonogram puzzles for any x*x size with given starting conditions.

    Some of this could likely be simplified and sped up by using NumPy.  However, I am trying to
    limit the number of requirements to make this easier to get up and running for people new to
    Python.  Also, this solves the nonograms that I tested with instantly and, as Donald Knuth said,
    "premature optimization is the root of all evil."

    Also, the tables could be stored internally as bit patterns to cut down on size as well as
    time from converting them back and forth.  As mentioned above though, this already runs fast
    enough and, at max, it supports 32x32 grids.  This would mean, at the largest, each table only
    needs to be 1K plus overhead per table.  Cutting this down to 128B plus overhead per table isn't
    really going to be noticeable on a modern system with GBs of RAM.
"""

import unittest
import webview

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
        # A filled out pattern was passed in, check to see if the current possibility is valid.
        temp_lines = []

        # Generate a bitmask from the pattern.
        mask = int(pattern, base=2)

        for line in lines:
            if (int(line, base=2) & mask) == mask:
                temp_lines.append(line)

            lines = temp_lines

    if len(lines[0]) == length and empty != '':
        # An empty position pattern was passed in, check to see if the current possibility is valid.
        temp_lines = []

        # Generate a bitmask from the empty positions.
        mask = int(empty, base=2)

        for line in lines:
            if not int(line, base=2) & mask:
                temp_lines.append(line)

            lines = temp_lines

    # Return the possible values.
    return lines

def find_overlap(length, patterns):
    """ This function finds the overlap between the current possibilities for a row or column. """

    # Set the initial masks to everything set.  This handles up to a 32x32 grid.
    overlap = 0xFFFFFFFF

    for pattern in patterns:
        # Convert each possibility to an integer based on the string bit pattern and generate
        # the overlap mask.
        overlap &= int(pattern, base=2)

    # Return the value as a bit pattern string.
    return '{0:b}'.format(overlap).zfill(length)

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

        Currently, passing in a partially solved puzzle is not supported.  The way nonograms are
        setup, it should never be required to have a partially solved puzzle to beging with unlike,
        for instance, sudokos.
    """

    # Initialize the existing tables.
    horizontal_existing = []
    vertical_existing = []

    # Initialize the backup tables.  These are used to compare with the current values in order to
    # see if the script has finished.  This is done instead of checking that every row and column
    # is correct because, if there is a bug or data entry issue, this could cause and endless loop.
    horizontal_backup = []
    vertical_backup = []

    # Initialize the empty tables.
    horizontal_empty = []
    vertical_empty = []

    for row in horizontal_grid:
        # Find the initial patterns for each row.
        patterns = find_options(length, row)

        # Find the initial filled out and empty values for each row.
        horizontal_existing.append(find_overlap(length, patterns))
        horizontal_empty.append(find_empty(length, patterns))

    for col in vertical_grid:
        # Find the initial patterns for each column.
        patterns = find_options(length, col)

        # Find the initial filled out and empty values for each column.
        vertical_existing.append(find_overlap(length, patterns))
        vertical_empty.append(find_empty(length, patterns))

    # Initialize the done flag as well as the number of passes needed to solve the puzzle.
    passes = 0
    done = 0

    while not done:
        # If changes were made to the grid, keep trying to solve the puzzle.

        # Set the backed-up data to the current data.
        horizontal_backup = horizontal_existing[:]
        vertical_backup = vertical_existing[:]

        # Update the existing tables based on their counterpart table.
        vertical_existing, horizontal_existing \
            = update_existing(horizontal_existing, vertical_existing)

        # Update the empty tables based on their counterpart table.
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
            horizontal_empty[index] = find_empty(length, patterns)

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
            vertical_empty[index] = find_empty(length, patterns)

        if (horizontal_existing == horizontal_backup and vertical_existing == vertical_backup):
            # Nothing changed on this last pass.  Set the flag to done so we do not end up in
            # and infinite loop.
            done = 1

        passes += 1

    print('Passes: %u\n\n' % passes)

    return horizontal_existing, horizontal_empty

def find_empty(length, potential):
    """ This function finds the empty positions based of the potential fill positions. """

    # Make a copy of the potential patterns.
    patterns = potential[:]

    for index, pattern in enumerate(patterns):
        # Flip the bits of each position.
        patterns[index] = ''.join('1' if bit == '0' else '0' for bit in pattern)

    # Find the overlap of the empty positions.
    empty = find_overlap(length, patterns)

    return empty


class TestCases(unittest.TestCase):
    """ This class contains the unit tests for the nonogram solver's functions. """

    def test_find_overlap(self):
        """
            This method verifies that the function to generate the overlap is functioning
            correctly.
        """

        length = 15

        patterns = [
            "111110111100000",
            "111110011110000",
            "111110001111000",
            "111110000111100",
            "111110000011110",
            "111110000001111",
            "011111011110000",
            "011111001111000",
            "011111000111100",
            "011111000011110",
            "011111000001111",
            "001111101111000",
            "001111100111100",
            "001111100011110",
            "001111100001111",
            "000111110111100",
            "000111110011110",
            "000111110001111",
            "000011111011110",
            "000011111001111",
            "000001111101111"
        ]

        correct = "000000000000000"
        result = find_overlap(length, patterns)

        self.assertEqual(result, correct)

        patterns = [
            "111110111100000",
            "111110011110000",
            "111110001111000",
            "111110000111100",
            "111110000011110",
            "111110000001111",
            "011111011110000",
            "011111001111000",
            "011111000111100",
            "011111000011110",
            "011111000001111",
            "001111101111000",
            "001111100111100",
            "001111100011110",
            "001111100001111",
            "000111110111100",
            "000111110011110",
            "000111110001111"
        ]

        correct = "000110000000000"
        result = find_overlap(length, patterns)

        self.assertEqual(result, correct)

    def test_find_empty(self):
        """
            This method verifies that the function to find the empty pattern for a row returns the
            correct value.
        """

        length = 5
        potential = ["001111100111100"]
        correct = "110000011000011"

        empty = find_empty(length, potential)

        self.assertEqual(empty, correct)

    def test_update_existing(self):
        """
            This method verifies that the function to update the horizontal hash based on the data
            in the vertical hash and vice-versa returns the correctly updated hashes.
        """

        horizontal_before = [
            "001000000000000",
            "001000010000000",
            "000000010000000",
            "001000000000000",
            "101111100000000",
            "110011111100000",
            "001111111111000",
            "001110000000000",
            "001100000011100",
            "001100000100000",
            "001110000100111",
            "000110000000111",
            "000100010000000",
            "000000010000000",
            "000110000100000"
        ]

        vertical_before = [
            "000011000000000",
            "000001000000000",
            "110110111110000",
            "000010111111100",
            "000011110011000",
            "000011100000000",
            "000011100000000",
            "011001100000110",
            "000001100000000",
            "000001100110000",
            "000000100000000",
            "000000000000000",
            "000000000011000",
            "000000000011000",
            "000000000011000"
        ]

        horizontal_after = [
            "001000000000000",
            "001000010000000",
            "000000010000000",
            "001000000000000",
            "101111100000000",
            "110011111100000",
            "001111111111000",
            "001110000000000",
            "001100000011100",
            "001100000100000",
            "001110000100111",
            "000110000000111",
            "000100010000000",
            "000000010000000",
            "000110000100000"
        ]

        vertical_after = [
            "000011000000000",
            "000001000000000",
            "110110111110000",
            "000010111111101",
            "000011110011001",
            "000011100000000",
            "000011100000000",
            "011001100000110",
            "000001100000000",
            "000001100110001",
            "000000101000000",
            "000000101000000",
            "000000001011000",
            "000000000011000",
            "000000000011000"
        ]

        vertical_new, horizontal_new = update_existing(horizontal_before, vertical_before)

        self.assertTrue(horizontal_new == horizontal_after)
        self.assertTrue(vertical_new == vertical_after)

    def test_solve(self):
        """
            This method verifies that the function to solve the nonogram is functioning properly.
            It tests uses a known solvable, relatively complex, nonogram found in the wild.
        """

        length = 15

        horizontal_grid = [
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

        vertical_grid = [
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

        correct_solved = [
            "111000110000000",
            "101111010000000",
            "000000110000000",
            "001001100000000",
            "101111100000000",
            "110011111110000",
            "001111111111100",
            "011111000000110",
            "011110000011111",
            "011100000110001",
            "001110000100111",
            "000110011100111",
            "000110011100111",
            "000100110110110",
            "001111100111100"
        ]

        correct_empty = [
            "000111001111111",
            "010000101111111",
            "111111001111111",
            "110110011111111",
            "010000011111111",
            "001100000001111",
            "110000000000011",
            "100000111111001",
            "100001111100000",
            "100011111001110",
            "110001111011000",
            "111001100011000",
            "111001100011000",
            "111011001001001",
            "110000011000011"
        ]

        solved, empty = solve(length, horizontal_grid, vertical_grid)

        self.assertEqual(solved, correct_solved)
        self.assertEqual(empty, correct_empty)

def main():
    """ This is the main function of the program. """

    window = webview.create_window("Nonogram Solver", "web/main.html")

    window.expose(solve)

    webview.start(http_server=True)

if __name__ == '__main__':
    TESTS = unittest.main(exit=False)

    if TESTS.result.wasSuccessful():
        main()
    else:
        print("Exiting because tests failed.")
