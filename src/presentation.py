import typing as t
from src.commands import Command
import os

class Option():
    def __init__(self, name:str, command: Command, prep_cal: t.Optional[t.Callable] = None):
        self.name = name
        self.command = command
        self.prep_cal = prep_cal

    def choose(self):
        data = self.prep_cal() if self.prep_cal else None
        result = self.command.execute(data) if data else self.command.execute()
        print(result)

    def __str__(self):
        return self.name

def print_options(options:t.Dict[str, Option]) -> None:
    for shortcut, option in options.items():
        print(f'({shortcut}) {option}')
    print()

def option_choice_is_valid(choice:str, options: t.Dict[str, Option]) -> bool:
    result = choice in options or choice.upper() in options
    return result

def get_option_choice(options: t.Dict[str, Option]) -> Option:
    choice = input("Choose an option: ")
    while not option_choice_is_valid(choice, options):
        print("Invalid choice")
        choice = input('Choose an option: ')
    return options[choice.upper()]

def clear_screen():
    clear_command = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear_command)

def get_user_input(label:str, required: bool = True) -> t.Optional[str]:
    value = input(f'{label}: ') or None
    while required and not value:
        value = input(f'{label}: ') or None
    return value

def get_new_item_data() -> t.Dict[str,str]:
    result = {
        'title': get_user_input('Title'),
        'url': get_user_input('URL'),
        'notes': get_user_input('Notes', None)
    }
    return result

def get_item_id() -> int:
    result = int(get_user_input("Enter a item ID"))
    return result