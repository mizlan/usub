from colorama import Fore, Back, Style

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

    def populate(self, elem):
        pass

if __name__ == '__main__':
    g = Testcase()
    print(g.display())
