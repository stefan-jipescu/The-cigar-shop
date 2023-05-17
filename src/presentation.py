import typing as t
from src.commands import Command
import os
from src.database import DatabaseManager
class Option():
    def __init__(self, name:str, command: Command, prep_cal: t.Optional[t.Callable] = None, val_prep_cal = None):
        self.name = name
        self.command = command
        self.prep_cal = prep_cal
        self.val_prep_cal = val_prep_cal
    def choose(self):
        if self.val_prep_cal:
            data = self.prep_cal(self.val_prep_cal)
        elif self.prep_cal:
            #data = self.prep_cal() if self.prep_cal else None
            data = self.prep_cal()
        else:
            data = None
        result = self.command.execute(data) if data else self.command.execute()
        if isinstance(result, list):
            for line in result:
                print(line)
        else:
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
    data_table_1 = {
        'stock': float(get_user_input('Stock')),
        'price': float(get_user_input('Price')),
        'note': get_user_input('Note', None)
    }

    data_table_2 = {
        'product_id': int(get_last_item_inserted()),
        'name': get_user_input('Name'),
        'ring': float(get_user_input('Ring size')),
        'length_': int(get_user_input('Length')),
        'origin': get_user_input('Origin country'),
        'other': get_user_input('Others details', None)
    }
    data_list = [data_table_1, data_table_2]
    return data_list

def get_last_item_inserted() -> int:
    db = DatabaseManager('cigar_db.db')
    cursor = db.select(
        table_name= 'items', 
        columns=['max(id)'])
    last_insert_id = ((cursor.fetchall())[0][0]) + 1
    return last_insert_id

def get_item_id() -> int:
    result = int(get_user_input("Enter the item ID"))
    return result

def update_stock( custom_stock: bool = False):
    product_id = {'id':get_item_id()}
    if custom_stock:
        column_value_set = {'stock': 0}
    else:
        column_value_set = {'stock': get_user_input('New stock')}
    data_tuple = [column_value_set, product_id]
    return data_tuple

def sell_product():
    id = get_item_id()
    pcs = int(get_user_input("Enter the number of sold pieces"))
    result = [id, pcs]
    return result

def update_description():
    print('please complete only the fields you wish to change')
    id = {'product_id': int(get_item_id())}
    edit_data = {
        'name': get_user_input('Name', None),
        'ring': get_user_input('Ring', None),
        'length_': get_user_input('Length_', None),
        'origin': get_user_input('Origin', None),
        'other': get_user_input('Other', None)
        }
    new_dict = { key: f"'{value}'" for key, value in edit_data.items() if value is not None}
    result = [id, new_dict]
    return result

def get_file_name():
    name = input("Insert the file name")
    return name