from tinydb import TinyDB, Query
from datetime import date
import sys
import os

from scrapeengines.avisos.Notificacions import Tipus_Notificacio
from scrapeengines.spiders.mathomcataleg import revisarfullcatalog
from scrapeengines.spiders.egdgamesofertes import revisarofertesegdgames
from scrapeengines.spiders.jugamosunacataleg import jugamosunafullcatalog
from runspiders import *

from colorama import Fore, Back, Style, init, deinit

dbofertes = TinyDB('db.json')

NEW_LINE = "\n"

def veureofertes():

    Cerca = Query()
                
    results = dbofertes.search(Cerca.status_stock == "NOU")

    print("JOCS NOUS: \n")
    for producte in results:
        print(producte['nom'])
        
    print("----------------\n")

    results = dbofertes.search(Cerca.status_preu == "REBAIXAT")

    print("JOCS REBAIXATS: \n")
    for producte in results:
        print(producte['nom'])
    print("----------------\n")
         
    results = dbofertes.search(Cerca.date_lastseen < date.today().isoformat())


    print("JOCS DESAPAREGUTS: \n")

    for producte in results:
        print(producte['nom'])
    print("----------------\n")     
     
    results = dbofertes.search(Cerca.stock != "Agotado")

     
    print("TOTAL STOCK / ESGOTATS: " )     
    print(str(len(results)) + "/" +str(len(dbofertes.all())))


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
    f.write("\"Nom\";\"Preu\";\"URL\"" + NEW_LINE)

    Cerca = Query()

    results = dbofertes.search(Cerca.stock != "Agotado")

    for producte in results:
        f.write(F"\"{producte['nom']}\";\"{producte['preu']}\";\"{producte['url']}\"" + NEW_LINE)

    f.close()
    print()
    print("FET!")
    print()


def extreurecatalegCSV():
    dbcataleg = TinyDB('dbcataleg.json')
    
    f= open(F"jocscataleg.csv","w", encoding='utf-8')
    f.write("\"Nom\";\"Preu\";\"URL\";\"STOCK\"" + NEW_LINE)

    Cerca = Query()

    #results = dbcataleg.search(Cerca.stock != "Agotado")
    results = dbcataleg.all()


    for producte in results:
        if not "preu" in producte: 
            producte['preu'] = 0
        if not "stock" in producte: 
            producte['stock'] = "N/A"           
        f.write(F"\"{producte['nom']}\";\"{producte['preu']}\";\"{producte['url']}\";\"{producte['stock']}\"" + NEW_LINE)
        
        
    print()
    print("FET!")
    print()
    f.close()


def mathomfullcatalog():
    revisarfullcatalog()
    

def deleteDB():
    print ("deleting!")
    #db.purge()

def egdgamesofertes():
    revisarofertesegdgames()

def mainmenu():
    os.system('cls')
    print(Style.RESET_ALL)
    
    print(Fore.WHITE + Back.BLUE)
    print("************MATHOM MENU**************")
    print(Style.RESET_ALL)
    choice = input("""
      1: Revisar ofertes
      2: Veure ofertes
      3: Treure CSV de ofertes
      PO: Purgar ofertes caducades
      
      4: Revisar cataleg complet
      5: Veure cataleg
      6: Treure CSV de cataleg   
      
      K: Delete DB
      Q: Sortir
    
      ?: """)

    if choice == "1":
        import subprocess
        subprocess.run(["python", "runspiders.py", "ofertesmathom"])
    elif choice == "2":
        veureofertes()
    elif choice == "3":
        extreureofertesCSV()
    elif choice == "PO" or choice =="po":
        purgarofertesdesaparegudes()              
    elif choice == "4":
        import subprocess
        subprocess.run(["python", "runspiders.py", "mathomcataleg"])
        subprocess.run(["python", "runspiders.py", "jugamosunacataleg"])
    elif choice == "5":
        veurecataleg()
    elif choice == "6":
        extreurecatalegCSV()
    elif choice == "777":
        egdgamesofertes()
    elif choice == "888":
        import subprocess
        subprocess.run(["python", "runspiders.py", "jugamosunacataleg"])
    elif choice == "K" or choice =="k":
        deleteDB()
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


    
   

