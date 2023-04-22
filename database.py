import sqlite3
import typing as t 


class DatabaseManager:
    def __init__(self, database_filename: str):
        """ Initializes the connection with the data base"""
        self.connection = sqlite3.connect(database_filename)
    
    def __del__(self):
        """Closes the connection with the data base"""
        self.connection.close()
    
    def _execute(self, statement: str, values: t.Optional[t.Tuple[str]] = None) -> sqlite3.Cursor:
        """Take a  statement and execute it with SQLite"""
        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute(statement, values or [])
                return cursor
        except sqlite3.IntegrityError:
            print(f'Something went wrong with the following transaction: \n{statement}')
            raise
    
    def create_table(self, table_name: str, columns: dict):
        columns_with_type = []
        for column_name, data_type in columns.items():
            current_column = f'{column_name} {data_type}'
            columns_with_type.append(current_column)
        statement_final = ", ".join(columns_with_type)
        query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {statement_final}
                );
            """
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
        placeholders = ", ".join(["?" * len(data.keys())])
        columns_values = tuple(data.values())
        query = f"""
            INSERT INTO
                {table_name} ({columns_name}) VALUES(
                    {placeholders}
                );
                """