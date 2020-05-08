import scrapy
from scrapeengines.items import Producte
from scrapy.loader import ItemLoader
from tinydb import TinyDB, Query
from datetime import date
from scrapy.crawler import CrawlerProcess

class EgdgamesOfertes(scrapy.Spider):
    name = "egdgames_ofertes"
    
 
       
    def start_requests(self):
        urls = [
            'https://www.egdgames.com/comprar/outlet/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)      
            

    def parse(self, response):
        db = TinyDB('dbegdgames.json')
       # page = response.url.split("/")[-2]
        #filename = 'quotes-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)
        
        for producteRAW in response.css('div.products div.product-small'):
            loader = ItemLoader(item=Producte(), selector=producteRAW)
            
            loader.add_css('nom', 'p.product-title a::text')
            #7
            # loader.add_css('editorial', '')
            loader.add_css('url', 'p.product-title a::attr(href)')
            loader.add_css('preu', 'span.price ins span.amount::text')
            loader.add_css('preu', 'span.price > span.amount::text')
            loader.add_css('preu_original', 'span.price del span.amount::text')
            loader.add_css('stock', 'p.stock::text')
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
                
            yield producte
 
        
        #PAGINES SEGÜENTS
        for next_page in response.css('link[rel=next]::attr(href)'):
            #print(next_page)
            pass
            yield response.follow(next_page, self.parse)
            
            
          #response.xpath("//meta[@name='keywords']/@content")[0].extract()
        
def revisarofertesegdgames():
    print ("fent ofertes egd...")
    
    process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': 'items.json'
    })

   
    process.crawl(EgdgamesOfertes)
    process.start() # the script will block here until the crawling is finished