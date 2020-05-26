import scrapy
from scrapeengines.items import Producte
from scrapy.loader import ItemLoader
from tinydb import TinyDB, Query
from datetime import date
from scrapy.crawler import CrawlerProcess
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from scrapy.utils.project import get_project_settings

class EgdgamesCataleg(scrapy.Spider):
    name = "egdgames_cataleg"

    def start_requests_test(self):
         urls = [
            'https://www.egdgames.com/comprar/oferta-semanal/'
         ]
         for url in urls:
             yield scrapy.Request(url=url, callback=self.parse)

    def start_requests(self):

        urls = [
            'https://www.egdgames.com/comprar/juegos-de-mesa/',
            'https://www.egdgames.com/comprar/juegos-de-importacion/',
            'https://www.egdgames.com/comprar/juegos-danados-o-desprecintados/',
            'https://www.egdgames.com/comprar/juegos-con-miniaturas/',
            'https://www.egdgames.com/comprar/oferta-semanal/',
            'https://www.egdgames.com/comprar/outlet/',
            'https://www.egdgames.com/comprar/juegos-de-mesa-de-segunda-mano/',
            'https://www.egdgames.com/comprar/sin-categorizar/page/4/'
            
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)      
            

    def parse(self, response):

        
        for producteRAW in response.css('div.products div.product-small'):
            loader = ItemLoader(item=Producte(), selector=producteRAW)
            
            loader.add_css('nom', 'p.product-title a::text')
            loader.add_css('url', 'p.product-title a::attr(href)')
            loader.add_css('preu', 'span.price ins span.amount::text')
            loader.add_css('preu', 'span.price > span.amount::text')
            loader.add_css('preu_original', 'span.price del span.amount::text')

            textstock = producteRAW.css('p.stock::text').get()
            if textstock == "Disponible":
                loader.add_value('stock','Disponible')
            else:
                loader.add_value('stock','Agotado')

            producte = loader.load_item()

            producte['botiga']='Egdgames'

            if producte['nom'] != "Blue Max":
                yield producte
                

        
        #PAGINES SEGÜENTS
        for next_page in response.css('link[rel=next]::attr(href)'):
            #print("next!")
            yield response.follow(next_page, self.parse)
            
  
          #response.xpath("//meta[@name='keywords']/@content")[0].extract()
        
def egdgamesfullcatalog():
    print ("fent catàleg...")
    

    process = CrawlerProcess(get_project_settings())  
    process.crawl(EgdgamesCataleg)
    process.start() # the script will block here until the crawling is finished
    