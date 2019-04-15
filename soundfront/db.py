import pyodbc
import os
from dotenv import load_dotenv


class Database:
    def __init__(self, server=None, database=None, username=None, password=None):
        load_dotenv()
        self.server = server or os.environ.get('DB_SERVER', default='localhost,1433')
        self.database = database or os.environ.get('DB_DATABASE', default='soundfront')
        self.username = username or os.environ.get('DB_USERNAME', default='sa')
        self.password = password or os.environ.get('DB_PASSWORD', default='')

    def connect(self):
        self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server +
                                   ';DATABASE=master'+';UID='+self.username+';PWD=' + self.password, autocommit=True)

        cursor = self.conn.cursor()
        cursor.execute(
            f"IF DB_ID(N'{self.database}') IS NULL CREATE DATABASE {self.database}")

    def destroy(self):
        cursor = self.conn.cursor()
        cursor.execute(f'DROP DATABASE {self.database}')

    def get_version(self):
        cursor = self.conn.cursor()
        cursor.execute('select @@version')
        row = cursor.fetchone()
        return row[0]
