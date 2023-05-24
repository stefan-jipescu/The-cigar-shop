from src import commands as c
from src import presentation as p


def loop():
    options = {
        "1":p.Option(
            name="Create new item",
            command=c.AddItemCommand(),
            prep_cal= p.get_new_item_data
        ),

        "2": p.Option(
            name = "Stock check",
            command = c.CheckStock(),
            prep_cal = p.get_item_id
        ),

        "3": p.Option(
            name = "Mark out of stock",
            command = c.UpdateStock(),
            prep_cal = p.update_stock,
            val_prep_cal= True
        ),

        "4": p.Option(
            name = "Update the stock",
            command = c.UpdateStock(),
            prep_cal = p.update_stock,
        ),

        "5": p.Option(
            name= "Sell a product",
            command=c.SellProduct(),
            prep_cal= p.sell_product
        ),

        "6": p.Option(
            name= "Update product details",
            command=c.UpdateDetails(),
            prep_cal= p.update_description
        ),

        "7":p.Option(
            name="Get details",
            command=c.ListItemsCommand(),
            prep_cal= p.get_item_id
        ),

        '8':p.Option(
            name="Export details",
            command=c.ExportToExcelCommand(),
            prep_cal= p.get_file_name
        ),

        '9':p.Option(
            name="Delete an item",
            command=c.DeleteItemCommand(),
            prep_cal= p.get_item_id
        ),

        '10':p.Option(
            name="Quit",
            command=c.QuitCommand()
        )
    }
    p.clear_screen()
    p.print_options(options)
    chosen_option = p.get_option_choice(options)
    p.clear_screen()
    chosen_option.choose()

    _ = input("Press ENTER to return to menu")
if __name__ =="__main__": 
    c.Create_new_table().execute()
    while True:
        loop()

