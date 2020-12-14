#! /usr/bin/python3

def find_options( length, filled ):
    total_filled = sum( filled )
    total_empty = length - total_filled
    extra = total_empty - len( filled ) + 1
    lines = []
    ones = filled[0]

    for pad in range( 0, extra + 1):
        line = ''
        blanks = len( filled )
        total_blanks = total_empty - pad

        line += '0' * pad
        line += '1' * ones

        blanks -= 1

        if blanks > 0:
            line += '0'

            total_blanks -= 1

        if len( filled ) > 1:
            subs = find_options( length - len( line ), filled[1:] )

            for sub in subs:
                lines.append( line + sub )
        else:
            line += '0' * total_blanks

            lines.append( line )

    return( lines )

def find_overlap( length, patterns ):
    overlap = 0xFFFFFFFF;

    for pattern in patterns:
        overlap &= int( pattern, base=2 )

    return( "{0:b}".format( overlap ).zfill( length ) )

def compare_existing( length, patterns, existing=''):
    if existing == '':
        existing = '0' * length

    pattern = int( find_overlap( length, patterns ), base=2 )

    pattern |= int( existing, base=2 )

    return( "{0:b}".format( pattern ).zfill( length ) )

def update_existing( from_existing, to_existing ):
    for row_index in range(0, len( from_existing ) ):
        for col_index in range(0, len( to_existing ) ):
            if from_existing[row_index][col_index] == '1':
                to_existing[col_index] = to_existing[col_index][:row_index] + '1' + to_existing[col_index][row_index+1:]

    return( to_existing )

length = 15

horizontal_grid = [
    [3,2],
    [1,4,1],
    [2],
    [1,2],
    [1,5],
    [2,7],
    [11],
    [5,2],
    [4,5],
    [3,2,1],
    [3,1,3],
    [2,3,3],
    [2,3,3],
    [1,2,2,2],
    [5,4]
]

vertical_grid = [
    [2,2],
    [1,1,3],
    [2,2,5,1],
    [1,1,9],
    [1,5,3,1],
    [1,5,1],
    [1,5,2],
    [3,2,3],
    [2,2],
    [2,6],
    [2,2,2],
    [1,1,1,],
    [3,5],
    [2,4],
    [5]
]

horizontal_existing = []
vertical_existing = []

horizontal_backup = []
vertical_backup = []

for row in horizontal_grid:
    patterns = find_options( length, row )

    horizontal_existing.append( find_overlap( length, patterns ) )

for row in vertical_grid:
    patterns = find_options( length, row )

    vertical_existing.append( find_overlap( length, patterns ) )

done = 0

while (not done):
    horizontal_backup = horizontal_existing[:]
    vertical_backup = vertical_existing[:]

    vertical_existing   = update_existing( horizontal_existing, vertical_existing   )
    horizontal_existing = update_existing( vertical_existing,   horizontal_existing )

    if (horizontal_existing == horizontal_backup and vertical_existing == vertical_backup):
        done = 1

for row in horizontal_existing:
    print( row )
