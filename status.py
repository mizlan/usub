#!/usr/bin/env python3

import json
import time
import sys

import requests
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
from alive_progress import alive_bar

import session
from submitutil import SubmissionID
from testcase import Testcase

def get_status(sid: SubmissionID):
    url = 'http://usaco.org/current/tpcm/status-update.php'
    data = {'sid': sid}
    cookies = session.get_cookie_dict()

    respdata = None
    attempts = 0
    max_iterations = 40
    spinner = ' ◢', '◣ ', '◤ ', ' ◥'

    with alive_bar(max_iterations, spinner='dots_waves') as bar:
        while True:
            attempts += 1
            response = requests.post(
                url,
                data=data,
                cookies=cookies
            )
            respdata = json.loads(response.text)
            status = respdata['sr']
            # print(spinner[attempts % 4], end='\r')
            if int(respdata['cd']) > -8:
                break
            bar()
            time.sleep(0.200)

    # print(respdata)
    if respdata['jd'].strip() == '':
        print(Fore.RED, end='')
        print(respdata['sr'].strip())
        print(respdata['output'].strip())
        print(Style.RESET_ALL)
        raise IOError('Error on submission.')
    soup = BeautifulSoup(respdata['jd'], 'lxml')
    return soup

def display_status(sid: SubmissionID):
    try:
        soup = get_status(sid)
    except IOError:
        sys.exit(1)

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
