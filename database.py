import sqlite3


class DatabaseManager:
    def __init__(self, database_filename: str):
        """ Initializes the connection with the data base"""
        self.connection = sqlite3.connect(database_filename)
    
    def __del__(self):
        """Closes the connection with the data base"""
        self.connection.close()
    
    def _execute(self, statement: str):
        """Take a statement and execute it with SQLite"""
        cursor = self.connection.cursor()
        cursor.execute(statement)
        return cursor
    
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
        print(query)
        self._execute(query)
