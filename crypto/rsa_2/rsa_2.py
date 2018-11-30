#!/usr/bin/env python
import gmpy2
from pwn import *
# N is very large, c is less than N.
# Public encryption is done like this: c = P**e % n     where P is plaintext, c is ciphertext, e is exponent, n is modulus (p*q)
# I feel like this is kind of guesswork, but if we assume P**3 (e is 3) is less than n, C is actually just P**3
# C = P**3 means the cubic root of C is P.
def exploit(c, e):
    plaintext_int = gmpy2.iroot(c, e)
    plaintext_hex = hex(plaintext_int[0])[2:] # remove 0x
    flag = unhex(plaintext_hex) # decode hex to ascii (pwntools)
    return flag 

if __name__ == "__main__":
    e = 3
    c = 2205316413931134031046440767620541984801091216351222789180535786851451917462804449135087209259828503848304180574549372616172217553002988241140344023060716738565104171296716554122734607654513009667720334889869007276287692856645210293194853
    flag = exploit(c, e)
    print flag 

