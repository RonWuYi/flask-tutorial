from flaskr.db import get_db


db = get_db()

list = db.execute('select * from files').fetchall()
for i in list:
    print(i)