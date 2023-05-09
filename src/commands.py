import typing as t
from src.database import DatabaseManager
from datetime import datetime
import sys
db = DatabaseManager('test.db')

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
    def execute(self, data: t.Dict[str, str]):
        date_added = datetime.utcnow().isoformat()
        data.setdefault("date_added", date_added)
        db.insert_data(table_name='items', data= data)
        return 'Bookmark added!'
    

class ListAllItemsCommand:
    def __init__(self, order_by: str = 'date_added'):
        self.order_by = order_by

    def execute(self):
        cursor = db.select(
            table_name = 'items',
            order_by=self.order_by
        )
        results = cursor.fetchall()
        return results

class DeleteItemCommand:
    def execute(self, data:int):
        db.delete(table_name = 'items', criteria= {'id':data})
        return "Item deleted"
    
class QuitCommand:
    def execute(self):
        sys.exit()