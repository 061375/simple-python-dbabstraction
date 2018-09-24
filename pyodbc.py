from tstpydb import tstpydb

''' 
CONNECT REMOTE
This connection stream will vary based on your avaiable drivers
'''
db = tstpydb.tstPyDb('_pyodbc',{
	"driver":"ODBC Driver 13 for SQL Server",
	"server":"192.168.xxx.xxx",
	"database":"myDatabase",
	"user":"myUsername",
	"password":"xxxxxxxxxxxxx"
})

'''
UPDATE myTable SET myColumn = 'myValue' WHERE Id = 100
'''
db.table('myTable').update({"myColumn":"myValue"}).where('Id','=','100')

'''
SELECT * FROM myTable

NOTE: Pass False to get() so that the connection doesn't pass self commit
		This is because with a SQL server database an insert or update requires a self commit but a select will error with that passed
'''
c = db.table('myTable').get(False)
for row in c:
    print('row = %r' % (row,))

print("_________________________________")

