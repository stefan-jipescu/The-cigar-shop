from src import commands as c
from src import presentation as p


def loop():
    options = {
        "A":p.Option(
            name="Add an item",
            command=c.AddItemCommand(),
            prep_cal= p.get_new_item_data,
        ),
        "B": p.Option(
            name= "List items by date",
            command=c.ListAllItemsCommand()
        ),
        "T":p.Option(
        name="List items by name",
        command=c.ListAllItemsCommand(order_by= 'title')
        ),
        'D':p.Option(
            name="Delete an item",
            command=c.DeleteItemCommand(),
            #prep_cal= p.get_item_id()
        ),
        'Q':p.Option(
            name="Quit",
            command=c.QuitCommand()
        )
    }
    p.clear_screen()
    p.print_options(options)
    chosen_option = p.get_option_choice(options)
    p.clear_screen()
    chosen_option.choose()
if __name__ =="__main__": 
    c.Create_new_table().execute()
    while True:
        loop()

