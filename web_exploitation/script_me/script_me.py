#!/usr/bin/env python3
import sys
from pwn import *
from functools import reduce
context.log_level = 50

# Check depth by replacing all () with nothing until nothing is left
def depth(s):
    count=0
    while(len(s)!=0):
        s = s.replace('()','')
        count+=1
    return count

# Kind of self explanatory but it checks for depth of each argument and absorbs or concatenates based on depth
def calc(s1,s2):
    if depth(s1) is depth(s2):
        return s1+s2
    if depth(s1) > depth(s2):
        return s1[:-1] + s2 + ')'
    if depth(s1) < depth(s2):
        return '(' + s1 + s2[1:]

# Solve runs calc on the first and second argument and stores it in the first until the list is at an end.
def solve(args):
    args = args.replace(' ','').split('+')
    result = args[0]
    for arg in args[1:]:
        result = calc(result, arg)
    return result

# Make a connection and automate the process
host = '2018shell3.picoctf.com'
port = '8672'
r = remote(host, port)
while True:
    try:
        lines=r.recvuntil(b'\n>').split(b'\n')
        equation=lines[-3].split(b'=')[0]
        r.sendline(solve(equation.decode('UTF-8')))
    except: 
        print(r.recv().decode('UTF-8').split(':')[1].strip())
        break
r.close()

    
    
