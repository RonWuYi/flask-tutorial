import os
import sqlite3

conn = sqlite3.connect('/home/hdc/project/github/flask-tutorial/instance/flaskr.sqlite')

c = conn.cursor()

mylist = c.execute(
    '''
    SELECT * from kms
    '''
).fetchall()
print(len(mylist))
for i in mylist:
    print(i)
conn.close()