from tinydb import TinyDB, Query

db = TinyDB('db.json')

#db.purge()

print (len(db.all()))