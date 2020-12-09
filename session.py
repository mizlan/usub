'''
handles session cookie invalidation/expiration, and retrieving cookie
'''

import os
import sys
import auth
from pathlib import Path

def get_authentication():
    return auth.get()

def get_token_path():
    return Path.home() / 'usub'

def _get_cached_cookie():
    '''
    gets cached cookie.
    checks environment variable 'USUB_TOKEN' and file '~/usub'.
    raises KeyError if neither is found.
    '''

    token = os.environ.get('USUB_TOKEN')
    tpath = get_token_path()

    if token is not None:
        return token
    if tpath.is_file():
        tpath = tpath.resolve(strict=True)
        return open(tpath).read().strip()

    raise KeyError

def write_cookie(cookie: str):
    os.environ['USUB_TOKEN'] = cookie
    tpath = get_token_path()
    with open(tpath, 'w+') as f:
        f.write(cookie + '\n')

def invalidate_cookie():
    '''
    uses try/except to avoid race conditions, see:
    https://en.wikipedia.org/wiki/Time-of-check_to_time-of-use
    '''

    try:
        del os.environ['USUB_TOKEN']
    except KeyError:
        sys.stderr.write('USUB_TOKEN not found\n')

    tpath = get_token_path()
    try:
        tpath.unlink()
    except FileNotFoundError:
        sys.stderr.write(f'{tpath} not found\n')

def get_session_cookie():
    cached = _get_cached_cookie()
    return cached

if __name__ == "__main__":
    # print(get_session_cookie())
    invalidate_cookie()
