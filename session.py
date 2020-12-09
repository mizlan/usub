'''
handles cookie invalidation/expiration, and retrieving cookie
'''

import os
import auth
from pathlib import Path

def get_authentication():
    return auth.get()

def _get_cached_cookie():
    '''
    gets cached cookie.
    '''
    
    token = os.environ.get('USUB_TOKEN')
    tpath = Path.home() / 'usub'
    
    if token is not None:
        return token
    if tpath.is_file():
        tpath = tpath.resolve(strict=True)
        return open(tpath).read().strip()

    raise KeyError
    
def get_session_cookie():
    cached = _get_cached_cookie()
    return cached

if __name__ == "__main__":
    print(get_session_cookie())
