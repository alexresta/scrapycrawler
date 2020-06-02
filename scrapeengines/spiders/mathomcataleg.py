import scrapy
from scrapeengines.items import Producte
from scrapy.loader import ItemLoader
from tinydb import TinyDB, Query
from datetime import date
from scrapy.crawler import CrawlerProcess
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from scrapy.utils.project import get_project_settings

class MathomCataleg(scrapy.Spider):
    name = "mathom_cataleg"
    #db = TinyDB('dbcataleg.json')
    #db = TinyDB('dbcataleg.json', storage=CachingMiddleware(JSONStorage))

    def start_requests_test(self):
         urls = [
            'https://mathom.es/es/3500-juegos-de-importacion'
         ]
         for url in urls:
             yield scrapy.Request(url=url, callback=self.parse)

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
            'https://mathom.es/es/283-magic-the-gathering'
            
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


            textstock = producteRAW.css('div.availability span::text').get()

            if textstock is not None and textstock.strip() == "Agotado":
                loader.add_value('stock','Agotado')
            else:
                loader.add_value('stock','Disponible')


            producte = loader.load_item()

            producte['botiga']='Mathom'
            if "preu" in producte:
                producte['preu'] = float(producte['preu']) * 0.95
            yield producte
                

        
        #PAGINES SEGÜENTS
        for next_page in response.css('a.subcategory-name'):
            #pass
            yield response.follow(next_page, self.parse)
            
  
          #response.xpath("//meta[@name='keywords']/@content")[0].extract()
        
def revisarfullcatalog():
    print ("fent catàleg...")
    

    process = CrawlerProcess(get_project_settings())  
    process.crawl(MathomCataleg)
    process.start() # the script will block here until the crawling is finished
    