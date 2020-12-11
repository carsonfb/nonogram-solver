#! /usr/bin/python3

def find_options_new( length, filled ):
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
            subs = find_options_new( length - len( line ), filled[1:] )

            for sub in subs:
                lines.append( line + sub )
        else:
            line += '0' * total_blanks

            lines.append( line )

    return( lines )

patterns = find_options_new( 15, [1, 1, 9] )

for pattern in patterns:
    print( pattern )
    print( "Bin: %u" % int( pattern, base=2 ) )

#find_options( '', 15, [2, 2, 1] )
