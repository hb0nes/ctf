#!/usr/bin/env python
import re

def findOffset(string):
    bracket=re.search('(?<=.{7}).', string).group()
    original_bracket='{'
    return ord(original_bracket) - ord(bracket)

def decode(char, shift):
    return chr(ord(char) + shift)

if __name__ == "__main__":
    ciphertext = "PICO#4&[C!ESA2?#I0H%R3?JU34?A2%N4?S%C5R%]"
    result = [decode(char, findOffset(ciphertext)) for char in ciphertext]
    print ''.join(result)

