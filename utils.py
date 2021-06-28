import shutil
from colorama import Fore, Style
import os

def center_text(text):
    return text.center(shutil.get_terminal_size().columns)

def color_text(text, color):
    return f'{color}{text}{Style.RESET_ALL}'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')