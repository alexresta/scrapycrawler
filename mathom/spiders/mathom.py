import scrapy
from mathom.items import Producte
from scrapy.loader import ItemLoader
from tinydb import TinyDB, Query
from datetime import date

class QuotesSpider(scrapy.Spider):
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
                producteDB['date_created'] = date.today().isoformat()
                producteDB['status'] = 'NOU'
                db.insert(producteDB)
            else:
                if producteDB['stock'] != producte['stock'] or  producteDB['preu'] != producte['preu']:
                    producte['date_updated'] = date.today().isoformat()
                    
                    db.upsert(dict(producte),Cerca.url == producte['url'])

                    print ("Changed!")
            
                    print (producteDB)
            
            #db.upsert(dict(producte),Cerca.nom == producte['nom'])
            #db.upsert(dict(producte),cerca.url == producte['url'])
            #yield producte
 
        
        #PAGINES SEGÜENTS
#       for next_page in response.css('a[rel=next]'):
#           yield response.follow(next_page, self.parse)
            
            
          #response.xpath("//meta[@name='keywords']/@content")[0].extract()

