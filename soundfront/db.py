import pyodbc
import os


class Database:

    def __init__(self):
        # ideally, get these params from config
        self.server = os.environ.get('DB_SERVER', default='localhost,1433')
        self.database = os.environ.get('DB_DATABASE', default='TestDB')
        self.username = os.environ.get('DB_USERNAME', default='SA')
        self.password = os.environ.get('DB_PASSWORD', default='')

    def connect(self):
        self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server +
                                   ';DATABASE='+self.database+';UID='+self.username+';PWD=' + self.password)

    def get_version(self):
        cursor = self.conn.cursor()
        cursor.execute('select @@version')
        row = cursor.fetchone()
        return row[0]
