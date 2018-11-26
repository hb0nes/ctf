#!/usr/bin/env python
from base64 import b64decode
from base64 import b64encode
from pwn import *
import re
import requests
context.log_level = 9001

START_RANGE = 10 # Lower is more agressive, and a sure victory! Higher might be faster. It was 10 when writing this.
END_RANGE = 0 # Same as above
HOST = '2018shell3.picoctf.com'
PORT = '43731'
# This function flips all LSB bits in the cipher, one by one.
# It first decodes the cipher with base64 and then loops through each character, flipping LSB bits in the process.
# When set to max agressiveness, it'll fill the moddedCookies list with around 96 cookies, each character altered only once
# So: 45th modified cookie has character 45 modified
def bitFlip(cookie):
    moddedCookies = []
    cipher = b64decode(cookie)
    for k in range(START_RANGE, len(cipher) - END_RANGE):
        moddedCipher = ""
        for i in range(0, len(cipher)):
            if i == k:
                xoredChar = chr(ord(cipher[i]) ^ 1)
                moddedCipher += xoredChar
            else:
                moddedCipher += cipher[i]
        moddedCookies.append(b64encode(moddedCipher))
    return moddedCookies

# Gets you a vegan cookie. What a neat function!
def getCookie():
    r = requests.post('http://{}:{}/login'.format(HOST, PORT), data = {'user':'get','password':'rekt'}, allow_redirects=False)
    return r.cookies['cookie']

# Gets modded cookies and runs them by the server one by one,
# checking the response for any errors/flags
def exploit():
    moddedCookies = bitFlip(getCookie())
    count = 0
    for cookie in moddedCookies:
        count += 1
        r_cookie = dict(cookie=cookie)
        r = requests.get('http://{}:{}/flag'.format(HOST, PORT), cookies=r_cookie)
        flag = re.findall('picoCTF{.*}', r.text)
        if flag:
            print "Here's the flag: {}".format(flag[0])
            print "Winning cookie: {}".format(cookie)
            print "Times tried: {}".format(count)
            break
    if not flag:
        print "So sad, exploit doesn't work this way anymore."

if __name__ == "__main__":
    exploit()
