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

    return( "{0:b}\n".format( overlap ).zfill( length + 1 ) )

def compare_existing( length, patterns, existing ):
    pattern = int( find_overlap( length, patterns ), base=2 )

    pattern |= int( existing, base=2 )

    return( "{0:b}\n".format( pattern ).zfill( length + 1 ) )

patterns = find_options( 15, [1, 1, 9] )

for pattern in patterns:
    print( pattern )
    print( "Bin: %u" % int( pattern, base=2 ) )

print( "Overlap: %s" % find_overlap( 15, patterns ) )

print( "Existing: %s" % (compare_existing( 15, patterns, "111111111000000" )) )
