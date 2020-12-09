#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

import session
from submitutil import SubmissionID

def get_status(sid: SubmissionID):
    url = 'http://usaco.org/current/tpcm/status-update.php'
    data = {'sid': sid}
    cookies = session.get_cookie_dict()

    response = requests.post(
        url,
        data=data,
        cookies=cookies
    )

    print(type(response.text))
    # soup = BeautifulSoup(response.text, 'lxml')
    # print(soup)

if __name__ == '__main__':
    get_status('2217019')
