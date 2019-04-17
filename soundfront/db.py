import pyodbc
import textwrap
import os
from dotenv import load_dotenv


class Database:
    def __init__(self, server=None, database=None, username=None, password=None):
        load_dotenv()
        self.server = server or os.environ.get(
            'DB_SERVER', default='localhost,1433')
        self.database = database or os.environ.get(
            'DB_DATABASE', default='soundfront')
        self.username = username or os.environ.get('DB_USERNAME', default='sa')
        self.password = password or os.environ.get('DB_PASSWORD', default='')

    def connect(self):
        self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server +
                                   ';DATABASE=master'+';UID='+self.username+';PWD=' + self.password, autocommit=True)

        cursor = self.conn.cursor()
        cursor.execute(f"SELECT DB_ID(N'{self.database}')")
        db_exists = cursor.fetchone()

        if db_exists[0] is None:
            cursor.execute(f'CREATE DATABASE {self.database}')

        self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server +
                                   ';DATABASE='+self.database+';UID='+self.username+';PWD=' + self.password, autocommit=True)
        self.run_scripts()

    def run_scripts(self):
        cursor = self.conn.cursor()

        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

        for script in ['init.sql', 'user.sql']:
            script_path = os.path.join(ROOT_DIR, '../sql', script)
            batches = self.create_query_string(script_path).split("GO")

            for batch in batches:
                cursor.execute(batch)

    def destroy(self):
        cursor = self.conn.cursor()
        cursor.execute(f'DROP DATABASE {self.database}')
        self.conn.close()

    def get_version(self):
        cursor = self.conn.cursor()
        cursor.execute('select @@version')
        row = cursor.fetchone()
        return row[0]

    def create_query_string(self, sql_full_path):
        with open(sql_full_path, 'r') as f_in:
            lines = f_in.read()

            # remove any common leading whitespace from every line
            query_string = textwrap.dedent("""{}""".format(lines))

        return query_string
