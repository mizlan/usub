'''
handles session sessid invalidation/expiration, and retrieving sessid
'''

import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

import auth
import login

def get_authentication():
    return auth.get()

def get_cache_filepath():
    return Path.home() / 'usub'

def gen_new_sessid():
    username, password = get_authentication()
    sessid = login.login(username, password)
    return sessid

def _get_cached_sessid():
    '''
    gets cached sessid.
    checks file '~/usub' for key.
    raises KeyError if neither is found.
    '''

    tpath = get_cache_filepath()

    if tpath.is_file():
        tpath = tpath.resolve(strict=True)
        return open(tpath).read().strip()

    raise KeyError('nothing found')

def write_sessid(sessid: str):
    tpath = get_cache_filepath()
    with open(tpath, 'w+') as f:
        f.write(sessid + '\n')

def invalidate_sessid():
    '''
    uses try/except to avoid race conditions, see:
    https://en.wikipedia.org/wiki/Time-of-check_to_time-of-use
    '''

    tpath = get_cache_filepath()
    try:
        tpath.unlink()
    except FileNotFoundError:
        sys.stderr.write(f'{tpath} not found\n')

def get_sessid(force_invalidate=False):
    sessid = None
    if force_invalidate:
        invalidate_sessid()
    try:
        sessid = _get_cached_sessid()
        if not sessid_is_valid(sessid):
            sys.stderr.write('found invalid session ID')
            raise KeyError
    except KeyError:
        sessid = gen_new_sessid()
        write_sessid(sessid)
    return sessid

def get_cookie_dict():
    return {
        'PHPSESSID': get_sessid()
    }

def sessid_is_valid(sessid: str) -> bool:
    url = 'http://usaco.org/index.php'
    response = requests.get(
        url,
        cookies={ 'PHPSESSID': sessid }
    )
    return not ("Not currently logged in." in response.text)

if __name__ == '__main__':
    print(sessid_is_valid(_get_cached_sessid()))
