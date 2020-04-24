import scrapy
from mathom.items import Producte
from scrapy.loader import ItemLoader
from tinydb import TinyDB, Query
from datetime import date
from scrapy.crawler import CrawlerProcess

class MathomOfertes(scrapy.Spider):
    name = "mathom"
    
 
       
    def start_requests(self):
        urls = [
            'https://mathom.es/es/2507-ofertas?n=90'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)      
            

    def parse(self, response):
        db = TinyDB('db.json')
       # page = response.url.split("/")[-2]
        #filename = 'quotes-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)
        
        for producteRAW in response.css('div.category2507 div.product-container'):
            loader = ItemLoader(item=Producte(), selector=producteRAW)
            
            loader.add_css('nom', 'div.pro_second_box a.product-name::attr(title)')
            loader.add_css('editorial', 'p.pro_list_manufacturer::text')
            loader.add_css('url', 'div.pro_second_box a.product-name::attr(href)')
            loader.add_css('preu', 'span.price::text')
            loader.add_css('preu_original', 'span.old-price::text')
            loader.add_css('stock', 'div.availability span::text')
            producte = loader.load_item()
    
            Cerca = Query()
            
            results = db.search(Cerca.url == producte['url'])
            
            producteDB = results[0] if results else None
            
            
            if not producteDB:
                producte.init_new()
                
                db.insert(producte)
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
                        
                    db.upsert(dict(producteDB),Cerca.url == producte['url'])
                

 
        
        #PAGINES SEGÜENTS
        for next_page in response.css('a[rel=next]'):
            pass
            yield response.follow(next_page, self.parse)
            
            
          #response.xpath("//meta[@name='keywords']/@content")[0].extract()
        
def revisarofertes():
    print ("fent ofertes...")
    
    process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': 'items.json'
    })

   
    process.crawl(MathomOfertes)
    process.start() # the script will block here until the crawling is finished