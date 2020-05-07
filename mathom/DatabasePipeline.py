from scrapy.exceptions import NotConfigured
import scrapy
from mathom.items import Producte
from scrapy.loader import ItemLoader
from tinydb import TinyDB, Query
from datetime import date
from scrapy.crawler import CrawlerProcess
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

class DatabasePipeline(object):

    def open_spider(self, spider):
        print("OPEN!")
		self.db = TinyDB('dbcataleg.json', storage=CachingMiddleware(JSONStorage))


    def process_item(self, item, spider):
		self.db.insert(item)
        
    Cerca = Query()
            
        results = self.db.search(Cerca.url == producte['url'])
        
        producteDB = results[0] if results else None
        
        print("Producte: "+ producte['nom'])
        
        if not producteDB:
            producte.init_new()
            
            self.db.insert(producte)
        else:
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
        return item


    def close_spider(self, spider):
        self.db.close()
		
		
    