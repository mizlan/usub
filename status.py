#!/usr/bin/env python3

import json

import requests
from bs4 import BeautifulSoup

import session
from submitutil import SubmissionID
from testcase import Testcase

def get_status(sid: SubmissionID):
    url = 'http://usaco.org/current/tpcm/status-update.php'
    data = {'sid': sid}
    cookies = session.get_cookie_dict()

    response = requests.post(
        url,
        data=data,
        cookies=cookies
    )

    data = json.loads(response.text)
    soup = BeautifulSoup(data['jd'], 'lxml')

    return soup

def display_status(sid: SubmissionID):
    soup = get_status(sid)

    testcases = []
    for i in soup.find_all('a', class_='masterTooltip'):
        d = i.select_one('div')
        tc = Testcase()
        tc.populate(d)
        testcases.append(tc)

    for i in testcases:
        print(i.display())

if __name__ == '__main__':
    display_status('2217019')
