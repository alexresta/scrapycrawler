from tinydb import TinyDB, Query
from datetime import date


db = TinyDB('db.json')

#db.purge()

Cerca = Query()
            
results = db.search(Cerca.status_stock == "NOU")

print("JOCS NOUS: \n")
for producte in results:
    print(producte['nom'])
    
print("----------------\n")

results = db.search(Cerca.status_preu == "REBAIXAT")

print("JOCS REBAIXATS: \n")
for producte in results:
    print(producte['nom'])
print("----------------\n")
     
results = db.search(Cerca.date_lastseen < date.today().isoformat())

print("JOCS DESAPAREGUTS: \n")
for producte in results:
    print(producte['nom'])
print("----------------\n")     
     
print("TOTAL: " )     
print(len(db.all()))