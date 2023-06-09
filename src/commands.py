import typing as t
from src.database import DatabaseManager
import sys
from tabulate import tabulate
import openpyxl
from pathlib import Path
from jira import JIRA
import datetime

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
                'stock': 'INTEGER not null',
                'price': 'INTEGER not null',
                'note': 'text'
            }
        )
        db.create_table(
            table_name = 'details',
            columns ={
                "product_id": 'INTEGER',
                "name": 'TEXT NOT NULL',
                "ring": 'NUMERIC NOT NULL',
                "length_": 'INTEGER NOT NULL',
                "origin": 'TEXT NOT NULL',
                "other": 'TEXT'
            },
            primary_table = 'items',
            primary_column = 'id'
        )
class AddItemCommand:
    def execute(self, data: tuple):
        first_table_data = data[0]
        second_table_data = data [1]
        db.insert_data(table_name='items', data= first_table_data)
        db.insert_data(table_name='details', data= second_table_data)
        return 'Item added!'
    

class ListItemsCommand:
    def execute(self, data):
        columns = ('id', 'stock', 'name', 'ring', 'length_', 'origin')
        id_set = {'id': data}
        cursor = db.select(
            table_name = 'items',
            second_table_name = 'details',
            first_table_join_column = 'id',
            second_table_join_column = 'product_id',
            columns = columns,
            criteria = id_set,
        )
        results = cursor.fetchall()
        final_result = tabulate([columns, results[0]], tablefmt="grid")
        return final_result

class DeleteItemCommand:
    def execute(self, data:int):
        db.delete(table_name = 'items', criteria= {'id':data})
        db.delete(table_name = 'details', criteria= {'product_id':data})
        return "Item deleted"
    
class UpdateStock:
    def execute(self, data: list):
        id = data[1]
        values_set = data[0]
        if int([i for i in values_set.values()][0]) == 0:
            CreateJiraTicket(int([i for i in id.values()][0])).execute()
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
            return "The stock is too low for this sale"
        values_set = {'stock': new_stock}
        id_dict = {'id' : id}
        db.update(table_name = 'items', column_value = values_set, criteria = id_dict)
        if new_stock == 0:
            CreateJiraTicket(id).execute()
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

class ExportToExcelCommand:
    def execute(self, data:str) -> str:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        columns = ('id', 'stock', 'name', 'ring', 'length_', 'origin')
        cursor = db.select(
            table_name = 'items',
            second_table_name = 'details',
            first_table_join_column = 'id',
            second_table_join_column = 'product_id',
            columns = columns
        )
        results = cursor.fetchall()
        final_results = [columns] + results
        for row in final_results:
            sheet.append(row)
        export_folder_path = Path(f'./exports')
        export_folder_path.mkdir(parents = True, exist_ok=True)
        workbook.save(export_folder_path / f'{data}.xlsx')
        return 'done'

class QuitCommand:
    def execute(self):
        sys.exit()

class CreateJiraTicket():
    def __init__(self, id) -> None:
        self.id = id

    def execute(self) :
        time = datetime.datetime.today()
        api_token = 'ATATT3xFfGF0EX_UsCTgkZRokLYqR0dTZr4YxY0DwgZtQ54pzJh9q9SBCy9S-6NNLFNxevzhpt2exvMc8qLwPKM0kX5tE6_96vNq413TEHv88DL355c8UcCx40ehy23FY_F7wkeIt-k-kalRiwHrr6MbCFgUrQP3nMLsvIdZ01IMWTf3mDwO5JU=9E01A8F8'
        jira_connection = JIRA(
            basic_auth=('stefan_jipi@yahoo.com', api_token),
            server="https://justtests.atlassian.net"
        )

        issue_dict = {
            'project': {'key': 'MYF'},
            'summary': f'ID {self.id} is out of stock',
            'description': f'The ID {self.id} is out of stock from {time}',
            'issuetype': {'name': 'Task'},
        }

        jira_connection.create_issue(fields=issue_dict)
        return 'Ticket was created'