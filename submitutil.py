from enum import Enum

class Lang(Enum):
    C = '1'
    CPP = '2'
    CPP11 = '6'
    JAVA = '9'
    PASCAL = '8'
    PY2 = '3'
    PY3 = '4'

SubmissionID = str

def get_code(lang: str) -> Lang:
    '''
    get code from command line flag `lang'
    '''
    return {
        'c': Lang.C,
        'cpp': Lang.CPP,
        'cpp11': Lang.CPP11,
        'java': Lang.JAVA,
        'pascal': Lang.PASCAL,
        'py': Lang.PY3,
        'py2': Lang.PY2
    }[lang]

def infer(file_ext: str) -> Lang:
    return {
        'c': Lang.C,
        'cpp': Lang.CPP11,
        'java': Lang.JAVA,
        'pas': Lang.PASCAL,
        'py': Lang.PY3,
    }[file_ext]
