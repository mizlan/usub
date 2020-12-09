from colorama import Fore, Back, Style
import stdiomask

def get():
    username_prompt = f'{Fore.YELLOW}[username]{Style.RESET_ALL} '
    password_prompt = f'{Fore.CYAN}[password]{Style.RESET_ALL} '

    username = input(username_prompt)
    password = stdiomask.getpass(password_prompt)

    return username, password

if __name__ == "__main__":
    print(get())
