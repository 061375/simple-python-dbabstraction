import sys
'''
simpleDB @class
	simple database abstraction
	@version 1.0.2
	@author Jeremy Heminger <jeremy@tstwater.com> <contact@jeremyheminger.com>
'''
class simpleDB():

	def __init__(self, driver, connectionString):
		if driver == '_pymssql':
			self.conn = _pymssql(connectionString).get_conn()
		elif driver == '_pyodbc':
			self.conn = _pyodbc(connectionString).get_conn()
		else:
			print("Error: Requested driver was not found")
			sys.exit()
		self.cursor = self.conn.cursor()
	'''
	@param self
	@param string
	'''
	def execute(self, sql, commit=True):
		try:
			self.cursor.execute(sql)
			if commit:
				self.conn.commit()
		except Exception as e:
			print(e)
		return self
	'''
		@param self
		@param string - table
		@param list - cols - id,title,date,...
		@param dictionary - Example:
			{
				1:{"key":"id","oper":"=","value":"33","andor":"AND"},
				2:{"key":"id","oper":"=","value":"33","andor":""}
			}
	'''
	def select(self, table, cols, where, commit=False):
		sql = "SELECT "
		for col in cols:
			sql += col+","
		sql = sql[:-1]
		sql += " FROM "+table
		if not where:
			sql += ""
		else:
			sql += " WHERE "
			for wrow in where.items():
				for row in wrow.items():
					if "" == row['andor']:
						row['andor'] = "     "
					sql += row['key']+" "+row['oper']+" "+row['value']+"'  "+row['andor']+" "
			sql = sql[:-5]

		return self.execute(sql,commit)
	'''
		@param self
		@param string - table
		@param list - cols - id,title,date,...
		@param dictionary - Example:
			{
				"temp":"100"
			},
			{
				"machine":"enviropiI"
			}
	'''
	def update(self, table, update, where,commit=True):
		sql = "UPDATE "+table+" SET "
		for key, value in update.items():
			if unicode(value,'utf-8').isnumeric():
				sql += key+"="+value+","
			else:
				sql += key+"='"+value+"',"
		sql = sql[:-1]
		sql += " WHERE "
		for key, value in where.items():
			# make sure the right data type is being created

			if unicode(value,'utf-8').isnumeric():
				sql += key+"="+value+" AND"
			else:
				sql += key+"='"+value+"' AND"
		sql = sql[:-3]
		'''
		@todo
		for wrow in where.items():
			for row in wrow.items():
				if "" == row['andor']:
					row['andor'] = "     "
				sql += row['key']+" "+row['oper']+" "+row['value']+"'  "+row['andor']+" "
		sql = sql[:-5]
		'''
		#print(sql)
		return self.execute(sql,commit)
	'''
		gets the result from the query
	'''
	def get(self):
		return self.cursor
	'''
		close the connection
	'''
	def close():
		self.conn.close()



'''
	SUB CLASSES
'''

'''
@class _pymssql
'''
class _pymssql():
	def __init__(self, cs):
		import pymssql
		self.conn = pymssql.connect(cs['server'],cs['user'],cs['password'],cs['database'])
	def get_conn(self):
		return self.conn;

'''
@class _pyodbc
'''
class _pyodbc():
	def __init__(self, cs):
		import pyodbc
		cs = "Driver={"+cs['driver']+"};server="+cs['server']+";database="+cs['database']+";uid="+cs['user']+";pwd="+cs['password']
		#print(cs)
		self.conn = pyodbc.connect(cs)
	def get_conn(self):
		return self.conn
	def drivers():
		return pyodbc.drivers()
'''
@class _oracle
	###### NOTE ! ######
	-- This is untested and should NOT be used
'''
class _oracle():
	def __init__(self, cs, pooled = False):
		import cx_Oracle
		if pooled:
			self.conn = cx_Oracle.connect(cs['user'],cs['password'],cs['database'], cclass = "HOL", purity = cx_Oracle.ATTR_PURITY_SELF)
		else:
			self.conn = cx_Oracle.connect(cs)
	def get_conn(self):
		return self.conn;
'''
@class _sqlite
	###### NOTE ! ######
	-- This is untested and should NOT be used
'''
class _sqlite():
	def __init__(self, cs):
		import sqlite3 as lite
		self.conn = lite.connect(cs)
	def get_conn(self):
		return self.conn;

