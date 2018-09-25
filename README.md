# simple-python-dbabstraction
Simple Python Database Abstraction

## Features
### Database Connections
* pymssql
* pyodbc
* sqllite3

### Query Builder
Based on how a query is built in Laravel 5.x+
* table
* select
* update
* delete
* insert
* get
* execute

```
c = db.table('Users').where('Id','!=','3').where('Name','!=','Sonya').get()
for row in c:
    print('row = %r' % (row,))

print("_________________________________")
```

## TODO
I had an Oracle connection setup in the code using cx_Oracle but, I haven't tested it yet.

```
```
