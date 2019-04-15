import pyodbc
import os


class Database:

	def __init__(self):
		# ideally, get these params from config
		self.server = os.environ.get('DB_SERVER', default='localhost,1433')
		self.database = os.environ.get('DB_DATABASE', default='TestDB')
		self.username = os.environ.get('DB_USERNAME', default='SA')
		self.password = os.environ.get('DB_PASSWORD', default='')
		
		# if self.password is None:
			# throw errror

	def connect(self):
		cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
		self.cursor = cnxn.cursor()

	def get_version(self):
		self.cursor.execute('select @@version')
		row = self.cursor.fetchone()
		return row[0] 
