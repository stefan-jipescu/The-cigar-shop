import sqlite3


class DatabaseManager:
    def __init__(self, database_filename: str):
        """ Initializes the connection with the data base"""
        self.connection = sqlite3.connect(database_filename)
    
    def __del__(self):
        """Closes the connection with the data base"""
        self.connection.close()