#!/usr/bin/env python
import sys
from operator import itemgetter
from string import maketrans # translate table!





def count_letters(data):
    counted = [(x, data.count(x)) for x in map(chr, range(97,123))]
    counted.sort(key=itemgetter(1), reverse=True)
    return [letter for letter, index in counted]

def substitute_by_common(data, popular_letters, length):
    COMMON_LETTERS = ["e", "t", "a", "o", "i", "n", "s", "h", "r", "d", "l", "c", "u", "m", "w", "f", "g", "y", "p", "b", "v", "k", "j", "x", "q", "z"]
    # Create translate table
    old_string = ''.join(popular_letters[:length])
    print old_string
    new_string = ''.join(COMMON_LETTERS[:length])
    print new_string
    trans_table = maketrans(old_string, new_string)
    # Translate table
    mod_data = data.translate(trans_table)
    return mod_data

if __name__ == "__main__":
    ## Read file
    if len(sys.argv) > 1:
        file = open((sys.argv[1]), "r")
        data = file.read()
    else:
        quit()
    popular_letters = count_letters(data)
    mod_data = substitute_by_common(data, popular_letters, 7)
    # print mod_data
    