#!/usr/bin/env python
from pwn import *
HOST = "2018shell3.picoctf.com"
PORT = 36859
context.log_level = 500

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

def mulinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n

if __name__ == "__main__":
    r = remote(HOST, PORT)
    # Calculate N
    result = r.recvuntil('FEASIBLE').split('\n')
    q = int(result[6].split(':')[1].strip())
    p = int(result[7].split(':')[1].strip())
    r.sendline('y')
    r.sendafter('n:', str(p*q) + '\n')

    # Calculate q from n and p
    result = r.recvuntil('FEASIBLE').split('\n')
    p = int(result[4].split(':')[1].strip())
    n = int(result[5].split(':')[1].strip())
    r.sendline('y')
    r.sendafter('q:', str(n/p) + '\n')

    # Not feasible
    result = r.recvuntil('FEASIBLE').split('\n')
    r.sendline('n')

    # Calculate totient
    result = r.recvuntil('FEASIBLE').split('\n')
    q = int(result[4].split(':')[1].strip())
    p = int(result[5].split(':')[1].strip())
    r.sendline('y')
    r.sendafter('totient(n)', str((q-1) * (p-1)) + '\n')

    # Calculate ciphertext
    result = r.recvuntil('FEASIBLE').split('\n')
    plaintext = int(result[4].split(':')[1].strip())
    e = int(result[5].split(':')[1].strip())
    n = int(result[6].split(':')[1].strip())
    ciphertext = (plaintext**e) % n
    r.sendline('Y')
    r.sendafter('TIME TO FILL', str(ciphertext) + '\n')

     # Calculate totient
    result = r.recvuntil('FEASIBLE').split('\n')
    r.sendline('n')

    # Calculate private key
    result = r.recvuntil('FEASIBLE').split('\n')
    q = int(result[4].split(':')[1].strip())
    p = int(result[5].split(':')[1].strip())
    n = (q-1)*(p-1)
    e = int(result[6].split(':')[1].strip())
    r.sendline('Y')
    r.sendafter('d:', str(mulinv(e,n)) + '\n')
    
    # Calculate plaintext from cipher
    result = r.recvuntil('(Y/N):').split('\n')
    r.sendline('y')
    p = int(result[4].split(':')[1].strip())
    c = int(result[5].split(':')[1].strip())
    e = int(result[6].split(':')[1].strip())
    n = int(result[7].split(':')[1].strip())
    q = n/p
    n1 = (q-1) * (p-1)
    d = mulinv(e, n1)
    m = pow(c, d, n) # Was c**d%n before, but that is extremely slow.
    r.sendafter('plaintext:', str(m) + '\n')
    print unhex(hex(m)[2:])