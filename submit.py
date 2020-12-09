from pathlib import Path

import requests
from bs4 import BeautifulSoup

import session
import submitutil
from submitutil import Lang, SubmissionID

def submit(filepath: Path, lang: Lang, cpid: str) -> SubmissionID:
    url = 'http://usaco.org/current/tpcm/submit-solution.php'
    # url = 'https://httpbin.org/post'

    abspath = filepath.resolve(strict=True)

    data = {'cpid': cpid, 'language': lang.value}
    files = {'sourcefile': (filepath.name, open(abspath, 'rb'))}
    cookies = session.get_cookie_dict()

    response = requests.post(
        url,
        data=data,
        files=files,
        cookies=cookies
    )

    return get_sid(cpid)

def get_sid(cpid: str) -> SubmissionID:
    p_url = f'http://usaco.org/index.php?page=viewproblem2&cpid={cpid}'
    cookies = session.get_cookie_dict()

    response = requests.get(
        p_url,
        cookies=cookies
    )

    soup = BeautifulSoup(response.text, 'lxml')

    try:
        return soup.find(id='last-status').get('data-sid')
    except Exception as e:
        raise e

if __name__ == '__main__':
    g = Path('/Users/michaellan/code/cp/help-yourself.cpp')
    cpid = '1018'
    print(submit(g, submitutil.infer('cpp'), cpid))
