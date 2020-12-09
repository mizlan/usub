from colorama import Fore, Back, Style
from bs4 import BeautifulSoup

class Testcase:
    __slots__ = ['color', 'mem_usage', 'time_usage', 'display_char', 'testcase_num']
    
    def __init__(self):
        self.testcase_num = -1
        self.color = Fore.CYAN
        self.mem_usage = 'x'
        self.time_usage = 'x'
        self.display_char = '?'

    def display(self) -> str:
        return f'{self.testcase_num:>4} {self.color}[{self.display_char}]{Style.RESET_ALL}{self.time_usage:>11}{self.mem_usage:>10}'

    def populate(self, soup: BeautifulSoup):
        if 'trial-status-yes' in soup['class']:
            self.color = Fore.GREEN
        else:
            self.color = Fore.RED

        self.display_char = soup.select_one('div.res-symbol').text
        self.testcase_num = soup.select_one('div.trial-num').text

        if 'trial-status-yes' in soup['class']:
            info_soup = soup.select_one('div.info')
            self.mem_usage = info_soup.select_one('span:nth-child(1)').text
            self.time_usage = info_soup.select_one('span:nth-child(2)').text

if __name__ == '__main__':
    for i in range(10):
        g = Testcase()
        print(g.display())
