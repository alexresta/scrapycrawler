# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from tinydb import TinyDB, Query
from scrapeengines.items import Producte
from datetime import date

class MathomPipeline(object):
    def process_item(self, item, spider):
        return item

        
class DatabasePipeline(object):

    def open_spider(self, spider):
        print("OPEN!")
        self.db = TinyDB('dbcataleg.json', storage=CachingMiddleware(JSONStorage))


    def process_item(self, producte, spider):
        
        Cerca = Query()
            
        results = self.db.search(Cerca.url == producte['url'])
        
        producteDB = results[0] if results else None
        
        print("Producte: "+ producte['nom'])
        
        if not producteDB:
            producte.init_new()
            
            self.db.insert(producte)
        else:
            if not "date_lastseen" in producteDB: 
                producteDB['date_lastseen'] = '2000-01-01'
            if not "status_stock" in producteDB: 
                producteDB['status_stock'] = ''
            if not "status_preu" in producteDB: 
                producteDB['status_preu'] = ''                
            if not "preu" in producte: 
                producte['preu'] = 0
            if not "stock" in producte: 
                producte['stock'] = "N/A"           

            if producteDB['date_lastseen'] < date.today().isoformat():
                            
                producteDB['date_lastseen'] = date.today().isoformat()

                if producteDB['stock'] == 'Agotado' and producte['stock'] == 'En stock':
                    producteDB['status_stock'] = 'RESTOCK'
                    producteDB['stock'] = producte['stock']
                    producteDB['date_updated'] = date.today().isoformat()
                elif producteDB['stock'] == 'En stock' and producte['stock'] == 'Agotado':
                    producteDB['status_stock'] = 'ESGOTAT'
                    producteDB['stock'] = producte['stock']
                    producteDB['date_updated'] = date.today().isoformat()
                elif producteDB['status_stock'] == 'NOU':
                    producteDB['status_stock'] = 'STOCK'
                    producteDB['date_updated'] = date.today().isoformat()
                    
                if producteDB['preu'] >  producte['preu']:
                    producteDB['status_preu'] = 'REBAIXAT'
                    producteDB['preu'] = producte['preu']
                    producteDB['date_updated'] = date.today().isoformat()
                elif producteDB['preu'] <  producte['preu']:
                    producteDB['status_preu'] = 'FIPROMO'
                    producteDB['preu'] = producte['preu']
                    producteDB['date_updated'] = date.today().isoformat()
                elif producteDB['preu'] ==  producte['preu'] and producteDB['status_preu'] != "IGUAL":
                    producteDB['status_preu'] = 'IGUAL'
                    producteDB['date_updated'] = date.today().isoformat() 
                    
                self.db.upsert(dict(producteDB),Cerca.url == producte['url'])
        return producte


    def close_spider(self, spider):
        self.db.close()
        