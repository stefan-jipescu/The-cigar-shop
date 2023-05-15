import typing as t
#from typing import Any
#from typing_extensions import SupportsIndex
from src.database import DatabaseManager
from datetime import datetime
import sys
db = DatabaseManager('cigar_db.db')

class Command (t.Protocol):
    def execute():
        pass

class Create_new_table:
    def execute(self):
        db.create_table(
            table_name='items',
            columns={
                'id': 'integer primary key autoincrement',
                'title': 'text not null',
                'url': "text not null",
                'notes': 'text',
                "date_added": 'text not null'
            }
        )

class AddItemCommand:
    def execute(self, data: tuple):
        #: t.Tuple(t.Dict[str, str], t.Dict[str, str])
        #date_added = datetime.utcnow().isoformat()
        #data.setdefault("date_added", date_added)
        first_table_data = data[0]
        second_table_data = data [1]
        db.insert_data(table_name='items', data= first_table_data)
        db.insert_data(table_name='details', data= second_table_data)
        return 'Item added!'
    

class ListItemsCommand:
    def __init__(self, table_name: str, second_table_name: str = None, first_table_join_column: str = None, second_table_join_column: str = None,
        columns: list = None, criteria : t.Dict[str, str] = {}, order_by: t.Optional[str ] = None, ordered_descending: bool = False
        ):
        self.table_name = table_name
        self.second_table_name = second_table_name
        self.first_table_join_column = first_table_join_column
        self.second_table_join_column = second_table_join_column
        self.columns = columns
        self.criteria = criteria
        self.order_by = order_by
        self.ordered_descending = ordered_descending

    def execute(self, data):
        id_set = {'id': data}
        cursor = db.select(
            table_name = self.table_name,
            second_table_name = self.second_table_name,
            first_table_join_column = self.first_table_join_column,
            second_table_join_column = self.second_table_join_column,
            columns = self.columns,
            criteria = id_set,
            order_by = self.order_by,
            ordered_descending = self.ordered_descending
        )
        results = cursor.fetchall()
        return results

class DeleteItemCommand:
    def execute(self, data:int):
        db.delete(table_name = 'items', criteria= {'id':data})
        db.delete(table_name = 'details', criteria= {'product_id':data})
        return "Item deleted"
    
class UpdateStock:
    def execute(self, data: list):
        id = data[1]
        values_set = data[0]
        db.update(table_name = 'items', column_value = values_set, criteria = id)
        return 'Item updated'

class CheckStock:
    def execute(self, data: dict):
        cursor = db.select(
            table_name = 'items',
            columns = ['stock'],
            criteria = {'id': data}
            )
        results = int(((cursor.fetchall())[0][0]))
        return results

class SellProduct():
    def execute(self, data: dict):
        stock = CheckStock()
        id = data[0]
        pcs = int(data[1])
        old_stock = int(stock.execute(data = id))
        new_stock = (old_stock - pcs)
        if new_stock < 0:
            return "The stock is too low for thins sale"
        else:
            values_set = {'stock': new_stock}
            id_dict = {'id' : id}
            db.update(table_name = 'items', column_value = values_set, criteria = id_dict)
            return 'Sold'

class UpdateDetails():
    def execute(self, data):
        id = data[0]
        update_data = data[1]
        db.update(
            table_name = 'details',
            criteria = id,
            column_value = update_data
            )
        
        return 'Product updated'

class QuitCommand:
    def execute(self):
        sys.exit()