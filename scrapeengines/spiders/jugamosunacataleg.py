import scrapy
from scrapeengines.items import Producte
from scrapy.loader import ItemLoader
from tinydb import TinyDB, Query
from datetime import date
from scrapy.crawler import CrawlerProcess
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from scrapy.utils.project import get_project_settings

class JugamosunaCataleg(scrapy.Spider):
    name = "jugamosuna_cataleg"
    #db = TinyDB('dbcataleg.json')
    #db = TinyDB('dbcataleg.json', storage=CachingMiddleware(JSONStorage))

    def start_requests_test(self):
         urls = [
           # 'https://jugamosuna.es/tienda/3-juegos-de-mesa'
             'https://jugamosuna.es/tienda/1425-pre-venta'
        ]

    def start_requests(self):

        urls = [
            'https://jugamosuna.es/tienda/1438-estrategicos',
            'https://jugamosuna.es/tienda/4-familiares',
            'https://jugamosuna.es/tienda/8-infantiles-menor-de-12-anos',
            'https://jugamosuna.es/tienda/1451-juegos-de-importacion',
            'https://jugamosuna.es/tienda/1441-miniaturas',
            'https://jugamosuna.es/tienda/1425-pre-venta',
            'https://jugamosuna.es/tienda/1435-wargames'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)      
            

    def parse(self, response):
       # page = response.url.split("/")[-2]
        #filename = 'quotes-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)
        
        for producteRAW in response.css('li.product_item'):
            loader = ItemLoader(item=Producte(), selector=producteRAW)
            
            loader.add_css('nom', 'h3.product-title > a::attr(title)')
            loader.add_css('url', 'h3.product-title > a::attr(href)')
            loader.add_css('preu', 'button.product-price-and-shipping > span.price::text')

            disabled = producteRAW.css('button.product-price-and-shipping::attr(disabled)').get()
            if disabled is None:
                loader.add_value('stock','Disponible')
            else:
                loader.add_value('stock','Agotado')

            producte = loader.load_item()

            producte['botiga']='JugamosUna'
            yield producte
                

        
        #PAGINES SEGÜENTS
        for next_page in response.css('ul.page-list a[rel=next]::attr(href)'):
            #print("next!")
            yield response.follow(next_page, self.parse)
            pass
  

def jugamosunafullcatalog():
    print("fent catàleg...")

    process = CrawlerProcess(get_project_settings())
    process.crawl(JugamosunaCataleg)
    process.start()  # the script will block here until the crawling is finished
