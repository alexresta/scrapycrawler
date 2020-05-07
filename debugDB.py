from tinydb import TinyDB, Query
from datetime import date
import sys
import os
from mathom.spiders.mathomofertes import revisarofertes
from mathom.spiders.mathomcataleg import revisarfullcatalog
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
 
    input("Prem Enter per continuar")
    mainmenu()

def purgarofertesdesaparegudes():
    Cerca = Query()

    results = dbofertes.remove(Cerca.date_lastseen < date.today().isoformat())

    print("JOCS Esborrats: \n")
    for producte in results:
        print(producte)
    print("----------------\n") 
    
    input("Prem Enter per continuar")
    mainmenu()
 
def veurecataleg():
    dbcataleg = TinyDB('dbcataleg.json')
    
    Cerca = Query()
                
    results = dbcataleg.search(Cerca.status_stock == "NOU")

    print("JOCS NOUS: \n")
    for producte in results:
        print(producte['nom'])
        
    print("----------------\n")

    results = dbcataleg.search(Cerca.status_preu == "REBAIXAT")

    print("JOCS REBAIXATS: \n")
    for producte in results:
        print(producte['nom'])
    print("----------------\n")
         
    results = dbcataleg.search(Cerca.date_lastseen < date.today().isoformat())

    print("JOCS DESAPAREGUTS: \n")
    for producte in results:
        print(producte['nom'])
    print("----------------\n")     
     
    results = dbcataleg.search(Cerca.stock != "Agotado")

     
    print("TOTAL STOCK / ESGOTATS: " )     
    print(str(len(results)) + "/" +str(len(dbcataleg.all())))
 
    input("Prem Enter per continuar")
    mainmenu()
    

def extreureofertesCSV():

    f= open(F"jocsoferta.csv","w")
    f.write("\"Nom\";\"Preu\";\"URL\"" + NEW_LINE)

    Cerca = Query()

    results = dbofertes.search(Cerca.stock != "Agotado")

    for producte in results:
        f.write(F"\"{producte['nom']}\";\"{producte['preu']}\";\"{producte['url']}\"" + NEW_LINE)
        
        
    print()
    print("FET!")
    print()


    input("Prem Enter per continuar")
    mainmenu()
   
def extreurecatalegCSV():
    dbcataleg = TinyDB('dbcataleg.json')
    
    f= open(F"jocscataleg.csv","w")
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


    input("Prem Enter per continuar")
    mainmenu()
    
def mathomofertes():
    revisarofertes()
    
    input("Prem Enter per continuar")
    mainmenu()
  
def mathomfullcatalog():
    revisarfullcatalog()
    
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
        mathomofertes()
    elif choice == "2":
        veureofertes()
    elif choice == "3":
        extreureofertesCSV()
    elif choice == "PO" or choice =="po":
        purgarofertesdesaparegudes()              
    elif choice == "4":
        mathomfullcatalog()   
    elif choice == "5":
        veurecataleg()
    elif choice == "6":
        extreurecatalegCSV()       
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
    
   

