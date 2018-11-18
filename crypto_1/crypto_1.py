#!/usr/bin/env python
key = 'thisisalilkey'
secret = 'llkjmlmpadkkc'

def offset(s):
    return ord(s) - 97

def magic(s1, s2):
    if ord(s1) > ord(s2):
        return chr(abs(offset(s1) - (offset(s2) + 26)) + 65)
    return chr(abs(offset(s1) - offset(s2)) + 65)

def decode(key, secret):
    decoded = ""
    for i, char in enumerate(secret):
        print "{} -> {} = {}".format(key[i], char, magic(key[i], char))
        decoded += magic(key[i], char)
    return decoded

if __name__ == "__main__":
    if len(key) is not len(secret):
        print 'That shit aint the same length.'
        exit()
    else:
        print 'picoCTF{' + decode(key, secret) + '}'