#!/usr/bin/env python

# Tries 26 different variations of the string, it's literally the same as a rotational encoding (ROT) :\
def decrypt(s):
    msgs = []
    for i in range(1,27):
        dec = ""
        for char in s:
            if char.isalpha():
                if char.islower():
                    mod_char = chr((ord(char) - 97 + i) % 26 + 97)
                else:
                    mod_char = chr((ord(char) - 65 + i) % 26 + 65)
                dec += mod_char
            else:
                dec += char
        msgs.append(dec)
    return msgs

if __name__ == "__main__":
    msgs = decrypt('grpqxdllaliazxbpxozfmebotlvlicmr')
    print 'picoCTF{' + [m for m in msgs if 'justagoodold' in m][0] + '}'