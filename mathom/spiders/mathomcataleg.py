import scrapy
from mathom.items import Producte
from scrapy.loader import ItemLoader
from tinydb import TinyDB, Query
from datetime import date
from scrapy.crawler import CrawlerProcess
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

class MathomCataleg(scrapy.Spider):
    name = "mathomCataleg"
    #db = TinyDB('dbcataleg.json')
    db = TinyDB('dbcataleg.json', storage=CachingMiddleware(JSONStorage))

 
       
    def start_requests(self):   
        urls = [
            'https://mathom.es/es/244-juegos-de-tablero',
            'https://mathom.es/es/1831-juegos-familiares',
            'https://mathom.es/es/2965-juegos-infantiles',
            'https://mathom.es/es/427-juegos-de-cartas',
            'https://mathom.es/es/2160-juegos-de-dados',
            'https://mathom.es/es/2746-juegos-historicos-y-de-guerra',
            'https://mathom.es/es/1794-juegos-de-miniaturas',
            'https://mathom.es/es/3500-juegos-de-importacion',
            'https://mathom.es/es/242-juegos-de-cartas-coleccionables'
            
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)      
            

    def parse(self, response):
       # page = response.url.split("/")[-2]
        #filename = 'quotes-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)
        
        for producteRAW in response.css('div.center_column div.product-container'):
            loader = ItemLoader(item=Producte(), selector=producteRAW)
            
            loader.add_css('nom', 'div.pro_second_box a.product-name::attr(title)')
            loader.add_css('editorial', 'p.pro_list_manufacturer::text')
            loader.add_css('url', 'div.pro_second_box a.product-name::attr(href)')
            loader.add_css('preu', 'span.price::text')
            loader.add_css('preu_original', 'span.old-price::text')
            loader.add_css('stock', 'div.availability span::text')
            producte = loader.load_item()
    
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
                

        
        #PAGINES SEGÜENTS
        for next_page in response.css('a.subcategory-name'):
            #print("next!")
            yield response.follow(next_page, self.parse)
            
        db.storage.flush()    
          #response.xpath("//meta[@name='keywords']/@content")[0].extract()
        
def revisarfullcatalog(self):
    print ("fent catàleg...")
    
    process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': 'items.json'
    })

   
    process.crawl(MathomCataleg)
    process.start() # the script will block here until the crawling is finished
    db.close()
    