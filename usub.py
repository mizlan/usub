import re
import sys
from pathlib import Path

import colorama

import getargs
import session
import submit
import submitutil
import status

def main():
    args = getargs.getargs()

    TYPE = 'status'
    _prob = args.problem
    CPID = None

    match_link = re.search(r'cpid=(\d+)', _prob)
    match_cpid = re.match(r'(\d+)', _prob)
    if match_link is not None:
        CPID = match_link.group(1)
    elif match_cpid is not None:
        CPID = match_cpid.group(1)
    else:
        raise ValueError('Invalid CPID')

    # add for verbose in future
    # sys.stderr.write(f'found cpid of {CPID}\n')

    if args.fresh:
        session.invalidate_sessid()

    if args.file is not None:
        TYPE = 'submission'

    if TYPE == 'status':
        sid = submit.get_sid(CPID)
        status.display_status(sid)
    elif TYPE == 'submission':
        FILE = Path(args.file)
        LANG = args.lang
        CODE = None
        if not Path(FILE).is_file():
            raise FileNotFoundError(f'cant find file: {FILE}')
        if LANG == 'infer':
            FILEEXT = Path(FILE).resolve(strict=True).suffix.strip('.')
            CODE = submitutil.infer(FILEEXT)
        else:
            CODE = submitutil.get_code(LANG)
        sid = submit.submit(FILE, CODE, CPID)
        status.display_status(sid)

if __name__ == '__main__':
    colorama.init()
    main()
