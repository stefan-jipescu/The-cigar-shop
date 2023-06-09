import sqlite3
import typing as t 
from textwrap import dedent

class DatabaseManager:
    def __init__(self, database_filename: str):
        """ Initializes the connection with the data base"""
        self.connection = sqlite3.connect(database_filename)
    
    def __del__(self):
        """Closes the connection with the data base"""
        self.connection.close()
    
    def _execute(self, statement: str, values: t.Optional[t.Tuple[str]] = None) -> sqlite3.Cursor:
        """Take a  statement and optionally values for the placeholders, in order to execute it with SQLite"""
        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute(statement, values or [])
                return cursor
        except (sqlite3.IntegrityError, sqlite3.OperationalError, sqlite3.ProgrammingError):
            print(f'Something went wrong with the following transaction: \n{statement}')
            raise
    
    def create_table(self, table_name: str, columns: dict, primary_table: str = None, primary_column: str = None):
        columns_with_type = []
        for column_name, data_type in columns.items():
            current_column = f'{column_name} {data_type}'
            columns_with_type.append(current_column)
        statement_final = ", ".join(columns_with_type)
        query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {statement_final}
            """
        if primary_column and primary_table:
            #The foreign key must be the first column
            query += f""",CONSTRAINT fk_{primary_table}
            FOREIGN KEY({list(columns.keys())[0]})
            REFERENCES {primary_table}({primary_column}));"""
        else:
            query+=");"
        self._execute(query)
        


    def drop_table(self, table_name):
        """Take a table name and delete it"""
        query = f'DROP TABLE IF EXISTS {table_name};'
        self._execute(query)
    
    def insert_data(self, table_name: str, data: t.Dict[str, str]):
        """Takes a table name and INSERT the information from the dictionary where the key is 
        the columns and the value is the value 
        """
        columns_name = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data.keys()))
        columns_values = tuple(data.values())
        query = dedent(f"""
            INSERT INTO
                {table_name} (
                    {columns_name}
                ) VALUES (
                    {placeholders}
                );
        """)
        self._execute(query, columns_values)
    
    def delete(self, table_name: str, criteria: t.Dict[str, str]):
        '''Take a table name and delete the information based on the provided criteria'''
        placeholders = [f'{column} = ?' for column in criteria.keys()]
        delete_criteria = ' AND '.join(placeholders)
        delete_criteria_values = tuple(criteria.values())
        query = f'''
            DELETE FROM 
                {table_name}
            WHERE
                {delete_criteria};
        '''
        self._execute(query, delete_criteria_values)
    
    def select(self,
        table_name: str,
        second_table_name: str = None,
        first_table_join_column: str = None,
        second_table_join_column: str = None,
        columns: list = None,
        criteria : t.Dict[str, str] = {}, 
        order_by: t.Optional[str ] = None,
        ordered_descending: bool = False 
        ) -> sqlite3.Cursor:
        '''
        Takes in a table name and optionally a criteria as a dictionary, a column to order by and a boolean 
        flag to order it by that column descending or not 
        '''
        select_criteria_values = tuple(criteria.values())
        if columns:
            select_columns = ', '.join(columns)
            query = f'SELECT {select_columns} FROM {table_name}'
        else:
            query = f'SELECT * FROM {table_name}'
        if second_table_name:
            query += f' JOIN {second_table_name} ON {table_name}.{first_table_join_column} = {second_table_name}.{second_table_join_column}'
        if criteria:
            placeholders = [f'{column} = ?' for column in criteria.keys()]
            select_criteria = " AND ".join(placeholders)
            query = query + f' WHERE {select_criteria}'
        if order_by:
            query = query + f' ORDER BY {order_by}'
            if ordered_descending:
                query = query + ' DESC'
        query = query + ';'
        return self._execute(query, select_criteria_values)
    
    def update (self,
        table_name: str,
        column_value: t.Dict[str, str],
        criteria: t.Dict[str, str]
        ):
        '''Take a table name and update the information based on the provided criteria'''
        placeholders = [f'{column} = ?' for column in criteria.keys()]
        update_criteria = ' AND '.join(placeholders)
        update_criteria_values = tuple(criteria.values())
        set_values_list = [f'{column} = {value}' for column, value in column_value.items()]
        set_values = ", ".join(set_values_list)
        query = f'''
            UPDATE 
                {table_name}
            SET
                {set_values}
            WHERE
                {update_criteria};
        '''
        self._execute(query, update_criteria_values)