import sys
'''
simpleDB @class
	simple database abstraction
	@version 1.0.2
	@author Jeremy Heminger <jeremy@tstwater.com> <contact@jeremyheminger.com>
'''
class simpleDB():

	def __init__(self, driver, connectionString):
		self.commit = False
		# @var dictionary
		self.query = {
			"build":False,
			"table":None,
			"where":[],
			"orwhere":[],
			"update":[],
			"insert":[],
			"columns":[],
			"command":"select"
		}
		
		if driver == '_pymssql':
			self.conn = _pymssql(connectionString).get_conn()
		elif driver == '_pyodbc':
			self.conn = _pyodbc(connectionString).get_conn()
		elif driver == '_sqlite':
			self.conn = _sqlite(connectionString).get_conn()
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
		@param string
	'''
	def table(self, table):
		self.query['build'] = True
		self.query['table'] = table
		return self
	'''
		@param self
		@param list
	'''
	def select(self,columns):
		self.query['build'] = True
		self.query['columns'] = columns
		return self
	'''
		@param self
		@param dict {"column":"value"}
	'''
	def update(self, elem):
		self.query['build'] = True
		self.query['command'] = "update"
		self.query['update'].append(elem)
		return self	
	'''
		@param self
		@param dict {"column":"value"}
	'''
	def delete(self, elem):
		self.query['build'] = True
		self.query['command'] = "delete"
		return self	
	'''
	'''
	def insert(self, elem):
		self.query['build'] = True
		self.query['command'] = "insert"
		self.query['insert'].append(elem)
		return self	
	'''
		@param self
		@param string
		@param string
		@param mixed
		@param string
	'''
	def where(self,column,operator,value,_or=False):
		self.query['build'] = True
		self.query['where'].append([column,operator,value,_or])
		return self
	'''
		@param self

		@todo deal with TOP and LIMIT
		@todo nested
		@todo UNION
	'''
	def build(self):

		if self.query['command']=='select':
			sql = "SELECT "
			# do select
			if len(self.query['columns']) < 1:
				sql += '*'
			else:
				sql += ','.join(self.query['columns'])
			sql += ' FROM '+self.query['table']
			
		elif self.query['command']=='insert':
			self.commit = True
			# do insert
			sql = "INSERT INTO "+self.query['table']+" ("
			a = []
			b = []
			for _dict in self.query['insert']:
				for key,value in insdict.items():
					a.append(key)
					b.append(value)

			sql += ','.join(a)+") VALUES ('"+"','".join(b)+"')"

		elif self.query['command']=='update':
			self.commit = True
			# do update
			sql = "UPDATE "+self.query['table']+" SET "
			for _dict in self.query['update']:
				for key,value in _dict.items():
					if str(value).isnumeric():
						sql += key+"="+value+","
					else:
						sql += key+"='"+value+"',"
			sql = sql[:-1]
			
		else:
			# throw error
			print('Error: unknown command '+self.query['command'])

		if len(self.query['where']) > 0:
			# do where
			sql += ' WHERE '
			for value in self.query['where']:
				if False == value[3]:
					value[3] = "AND "
				else:
					value[3] = "OR "
				if str(value[2]).isnumeric():
					sql += value[0]+value[1]+value[2]+" "+value[3]
				else:
					sql += value[0]+value[1]+"'"+value[2]+"' "+value[3]
			sql = sql[:-4]
		
		# reset for the next query
		self.query = {
			"build":False,
			"table":None,
			"where":[],
			"orwhere":[],
			"update":[],
			"insert":[],
			"columns":[],
			"command":"select"
		}

		return sql
	'''
		gets the result from the query
	'''
	def get(self, selfcommit=None):
		if(not selfcommit is None):
			self.selfcommit = selfcommit
		# if the query is using the query builder
		if self.query['build']:
			self.execute(self.build(),self.commit)
			self.commit = False

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
'''
class _sqlite():
	def __init__(self, cs):
		import sqlite3 as lite
		self.conn = lite.connect(cs)
	def get_conn(self):
		return self.conn;


