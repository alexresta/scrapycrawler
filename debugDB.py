import pymongo
from tinydb import TinyDB, Query
from datetime import date
import sys
import os

import runspiders
from scrapeengines.avisos.Notificacions import Tipus_Notificacio

from runspiders import *

from colorama import Fore, Back, Style, init, deinit

from scrapeengines.pipelines import MongoDB
import scrapeengines.settings


dbofertes = TinyDB('db.json')

NEW_LINE = "\n"

def indexDB():
    settings = get_project_settings()

    mongo_server = settings.get('MONGODB_SERVER')
    mongo_db = settings.get('MONGODB_DB')
    mongo_port = settings.get('MONGODB_PORT')
    mongo_collection = settings.get('MONGODB_COLLECTION')

    mongoclient = pymongo.MongoClient(
            mongo_server,
            mongo_port
        )
    db = mongoclient.get_database(mongo_db).get_collection(mongo_collection)

    db.create_index([('nom', pymongo.TEXT)])

    pass

def purgarofertesdesaparegudes():
    Cerca = Query()

    results = dbofertes.remove(Cerca.date_lastseen < date.today().isoformat())

    print("JOCS Esborrats: \n")
    for producte in results:
        print(producte)
    print("----------------\n") 

 
def veurecataleg():
    dbnotificacions = TinyDB('dbavisos.json')
    dbcataleg = TinyDB('dbcataleg.json')

    Cerca = Query()

    results = dbnotificacions.search(Cerca.tipus_notificacio == Tipus_Notificacio.NOVETAT)

    print("JOCS NOUS: \n")
    for notificacio in results:
        print(notificacio['data'] + ' ' + notificacio['producte'] + ': ' + str(notificacio['preu_actual']) + ' - ' + notificacio['botiga'] )


    print("----------------\n")

    results = dbnotificacions.search(Cerca.tipus_notificacio == Tipus_Notificacio.REBAIXA)

    print("JOCS REBAIXATS: \n")
    for notificacio in results:
        print(notificacio['data'] + ' ' +  notificacio['producte'] + ': de ' + str(notificacio['preu_anterior']) + ' a ' + str(notificacio['preu_actual']) + ' - ' + notificacio['botiga'])


    print("----------------\n")

    results = dbnotificacions.search(Cerca.tipus_notificacio == Tipus_Notificacio.ENCAREIX)

    print("JOCS ENCARITS: \n")
    for notificacio in results:
        print(notificacio['data'] + ' ' + notificacio['producte'] + ': de ' + str(notificacio['preu_anterior']) + ' a ' + str(notificacio['preu_actual']) + ' - ' + notificacio['botiga'])

    print("----------------\n")

    results = dbnotificacions.search(Cerca.tipus_notificacio == Tipus_Notificacio.ESGOTAT)

    print("JOCS ESGOTATS: \n")
    for notificacio in results:
        print(notificacio['data'] + ' ' + notificacio['producte'] + ': ' + str(notificacio['preu_actual']) + ' - ' + notificacio['botiga'] )

    print("----------------\n")

    results = dbnotificacions.search(Cerca.tipus_notificacio == Tipus_Notificacio.RESTOCK)

    print("JOCS REESTOCK: \n")
    for notificacio in results:
        print(notificacio['data'] + ' ' + notificacio['producte'] + ': ' + str(notificacio['preu_actual']) + ' - ' + notificacio['botiga'] )


    print("----------------\n")

    dbcataleg.close()
    dbnotificacions.close()

    

def extreureofertesCSV():

    f= open(F"jocsoferta.csv","w", encoding='utf-8')
    f.write("\"Nom\";\"Preu\";\"Preu\";\"Botiga\"" + NEW_LINE)

    Cerca = Query()

    results = dbofertes.search(Cerca.stock != "Agotado")

    for producte in results:
        f.write(F"\"{producte['nom']}\";\"{producte['preu']}\";\"{producte['botiga']}\";\"{producte['url']}\"" + NEW_LINE)

    f.close()
    print()
    print("FET!")
    print()


def extreurecatalegCSV():
    dbcataleg = TinyDB('dbcataleg.json')
    
    f= open(F"jocscataleg.csv","w", encoding='utf-8')
    f.write("\"Nom\";\"Preu\";\"Botiga\";\"URL\";\"STOCK\"" + NEW_LINE)

    Cerca = Query()

    #results = dbcataleg.search(Cerca.stock != "Agotado")
    results = dbcataleg.all()


    for producte in results:
        if not "preu" in producte: 
            producte['preu'] = 0
        if not "stock" in producte: 
            producte['stock'] = "N/A"           
        f.write(F"\"{producte['nom']}\";\"{producte['preu']}\";\"{producte['botiga']}\";\"{producte['url']}\";\"{producte['stock']}\"" + NEW_LINE)
        
        
    print()
    print("FET!")
    print()
    f.close()


def deleteDBAvisos():

    choice = input("Segur? (S/N)")

    if choice == "S":
        os.remove("dbavisos.json")
        print("esborrat!")


def mainmenu():
    os.system('cls')
    print(Style.RESET_ALL)
    
    print(Fore.WHITE + Back.BLUE)
    print("************MATHOM MENU**************")
    print(Style.RESET_ALL)
    choice = input("""
  
      4: Revisar cataleg complet
      5: Veure cataleg
      6: Treure CSV de cataleg   
      
      DBI: crear índex DB
      DAV: Esborrar avisos de canvis
      Q: Sortir
    
      ?: """)

    if choice == "DBI":
        indexDB()
    elif choice == "333":
        extreureofertesCSV()
    elif choice == "PO" or choice =="po":
        purgarofertesdesaparegudes()
    elif choice == "4":
        allparallel()
    elif choice == "44":
        import subprocess
        start_time = time.time()

        subprocess.run(["python", "runspiders.py", "mathomcataleg"])
        subprocess.run(["python", "runspiders.py", "jugamosunacataleg"])
        subprocess.run(["python", "runspiders.py", "egdgamescataleg"])
        subprocess.run(["python", "runspiders.py", "zacatruscataleg"])
        print("--- TOTAL TIME: %s seconds ---" % (time.time() - start_time))

    elif choice == "5":
        veurecataleg()
    elif choice == "6":
        extreurecatalegCSV()

    elif choice == "888":
        import subprocess
        subprocess.run(["python", "runspiders.py", "jugamosunacataleg"])
    elif choice == "DAV":
        deleteDBAvisos()
    elif choice=="Q" or choice=="q":
        return True
    else:
        print()
        print()

        print(F"      {Fore.WHITE + Back.RED}Escull una opció del menú{Style.RESET_ALL}")

        print()

        input(F"      Prem {Fore.BLACK + Back.WHITE}RETORN{Style.RESET_ALL} per continuar")



init()
quit = False
while not quit:
    quit = mainmenu()
    if not quit:
        input("Prem Enter per continuar")

deinit()


    
   

