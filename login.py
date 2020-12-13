import json, re

import requests

def login(username: str, password: str) -> str:
    url = 'http://usaco.org/current/tpcm/login-session.php'
    data = { 'uname': username, 'password': password }
    response = requests.post(
        url,
        data=data
    )
    headers = response.headers
    data = json.loads(response.text)
    if data['msg'] == 'Incorrect password':
        raise KeyError('incorrect password!')
    return re.match(r'PHPSESSID=(\S+);', headers['Set-cookie']).group(1)

if __name__ == '__main__':
    username = input()
    password = input()
    print(login(username, password))
