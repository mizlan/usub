'''
handles session sessid invalidation/expiration, and retrieving sessid
'''

import sys
from pathlib import Path

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
    checks environment variable 'USUB_SESSID' and file '~/usub'.
    raises KeyError if neither is found.
    '''

    tpath = get_cache_filepath()

    if token is not None:
        return token
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

def get_sessid():
    cached = _get_cached_sessid()
    return cached

if __name__ == "__main__":
    write_sessid(gen_new_sessid())
    # print(get_sessid())
    # invalidate_sessid()
