#!/usr/bin/env python

def rot(s, times):
    LOW_BASE = 97
    UPP_BASE = 65
    ALPHABET_SIZE = 26
    dec = ""
    for char in s:
        if not char.isalpha():
            dec += char
        elif char.islower():
            dec += chr((ord(char)- LOW_BASE + times) % ALPHABET_SIZE + LOW_BASE)
        else:
            dec +=chr((ord(char)- UPP_BASE + times) % ALPHABET_SIZE + UPP_BASE)
    return dec

if __name__ == "__main__":
    print rot("cvpbPGS{guvf_vf_pelcgb!}", 13)