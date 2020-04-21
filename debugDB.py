from tinydb import TinyDB, Query
from datetime import date
import sys
import os
from mathom.spiders.mathom import revisarofertes
from colorama import Fore, Back, Style, init, deinit

db = TinyDB('db.json')
NEW_LINE = "\n"

def veureresultats():

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
     
    results = db.search(Cerca.stock != "Agotado")

     
    print("TOTAL STOCK / ESGOTATS: " )     
    print(str(len(results)) + "/" +str(len(db.all())))
 
    input("Prem Enter per continuar")
    mainmenu()
 

def extreureCSV():

    f= open(F"jocsoferta.csv","w")
    f.write("\"Nom\";\"Preu\";\"URL\"" + NEW_LINE)

    Cerca = Query()

    results = db.search(Cerca.stock != "Agotado")

    for producte in results:
        f.write(F"\"{producte['nom']}\";\"{producte['preu']}\";\"{producte['url']}\"" + NEW_LINE)
        
        
    print()
    print("FET!")
    print()


    input("Prem Enter per continuar")
    mainmenu()
    
def mathomofertes():
    revisarofertes()
    
    input("Prem Enter per continuar")
    mainmenu()
    
    
def deleteDB():
    print ("deleting!")
    #db.purge()
    input("Prem Enter per continuar")
    mainmenu()
    
    
def mainmenu():
    os.system('cls')
    print(Style.RESET_ALL)
    
    print(Fore.WHITE + Back.BLUE)
    print("************MATHOM MENU**************")
    print(Style.RESET_ALL) 

    choice = input("""
      1: Veure resultats
      2: Treure CSV de tot
      3: Revisar ofertes
      K: Delete DB
      Q: Sortir
    
      ?: """)

    if choice == "1":
        veureresultats()
    elif choice == "2":
        extreureCSV()
    elif choice == "3":
        mathomofertes()
    elif choice == "K" or choice =="k":
        deleteDB()
    elif choice=="Q" or choice=="q":
        deinit()
        sys.exit
    else:
        print()
        print()

        print(F"      {Fore.WHITE + Back.RED}Escull una opció del menú{Style.RESET_ALL}")

        print()

        input(F"      Prem {Fore.BLACK + Back.WHITE}RETORN{Style.RESET_ALL} per continuar")
        mainmenu()
    
  
init()  
mainmenu()
    
   

