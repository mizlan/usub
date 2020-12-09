import argparse

def getargs():
    parser = argparse.ArgumentParser(description='USACO Submission Client')
    parser.add_argument('--fresh', help='invalidate cookies and force fresh login', action='store_true')
    parser.add_argument('-f', '--file', help='submission file')
    parser.add_argument('-l', '--lang', help='submission language', default='infer')
    parser.add_argument(dest='problem', help='USACO problem link or cpid')
    args = parser.parse_args()
    print(args)

if __name__ == '__main__':
    getargs()
