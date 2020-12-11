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

def colorize(message: str) -> str:
    pref, suf = {
        'Waiting for Available Grading Server': (f'{Fore.MAGENTA}[', f']{Style.RESET_ALL}'),
        'Grading in Progress': (f'{Fore.CYAN}[', f']{Style.RESET_ALL}')
    }.get(message, ('', ''))

    return pref + message + suf

def get_status(sid: SubmissionID):
    if sid == '-1':
        raise KeyError('unattempted problem, no status!')

    url = 'http://usaco.org/current/tpcm/status-update.php'
    data = {'sid': sid}
    cookies = session.get_cookie_dict()

    last_status = ''
    respdata = None
    attempts = 0
    testcases = []
    max_iterations = 40

    # the number of the last completed testcase
    last_completed_test = 0

    while True:
        attempts += 1
        response = requests.post(
            url,
            data=data,
            cookies=cookies
        )
        respdata = json.loads(response.text)

        if 'jd' in respdata:
            soup = BeautifulSoup(respdata['jd'], 'lxml')
            for tc_elem in soup.find_all('a', class_='masterTooltip'):
                d = tc_elem.select_one('div')
                tc = Testcase()
                tc.populate(d)
                finished = int(tc.testcase_num)
                if finished > last_completed_test:
                    last_completed_test = finished
                    print(tc.display())
                testcases.append(tc)

        if 'cd' in respdata and int(respdata['cd']) > -8:
            break

        if 'sr' in respdata:
            status = respdata['sr']
            if status != last_status and respdata['jd'].strip() == '':
                print(colorize(status))
                last_status = status

        time.sleep(0.100)

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

if __name__ == '__main__':
    display_status('2217019')
