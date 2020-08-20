import scrapy
from scrapeengines.items import Producte
from scrapy.loader import ItemLoader
from tinydb import TinyDB, Query
from datetime import date
from scrapy.crawler import CrawlerProcess
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from scrapy.utils.project import get_project_settings
import logging


class JuguetestodayCataleg(scrapy.Spider):
    name = "juguetestoday_cataleg"
    #db = TinyDB('dbcataleg.json')
    #db = TinyDB('dbcataleg.json', storage=CachingMiddleware(JSONStorage))

    def start_requests_test(self):
         urls = [
            'https://juguetestoday.com/15-juegos-de-mesa?page=20'
         ]
         for url in urls:
             yield scrapy.Request(url=url, callback=self.parse)

    def start_requests(self):

        urls = [
            'https://juguetestoday.com/15-juegos-de-mesa?page=15',
            'https://juguetestoday.com/15-juegos-de-mesa?page=10',
            'https://juguetestoday.com/15-juegos-de-mesa?page=5',
            'https://juguetestoday.com/15-juegos-de-mesa'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        #page = response.url.split("/")[-2]
        #filename = 'quotes-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)
        
        for producteRAW in response.css('div.products article.product-miniature'):

            hidden = producteRAW.css('a.delete').get()
            if hidden is None:
                loader = ItemLoader(item=Producte(), selector=producteRAW)
                loader.add_css('nom', 'div.product-description h3.product-title > a::text')
                loader.add_css('url', 'div.product-description h3.roduct-title > a::attr(href)')
                loader.add_css('preu', 'div.product-price-and-shipping span.price::text')
                loader.add_css('preu_original', 'div.product-price-and-shipping span.regular-price::text')

                agotado = producteRAW.css('div#product-availability i.product-unavailable').get()
                if agotado is None:
                    loader.add_value('stock','Disponible')
                else:
                    loader.add_value('stock','Agotado')

                producte = loader.load_item()

                producte['botiga']='Juguetestoday'



                yield producte


        
        #PAGINES SEGÜENTS
        for next_page in response.css('div.pagination-nav a[rel=next]::attr(href)'):
            #print("next!")
            yield response.follow(next_page, self.parse)
            pass
  

def juguetestodaycatalog():
    print("fent catàleg...")

    process = CrawlerProcess(get_project_settings())
    process.crawl(JuguetestodayCataleg)
    process.start()  # the script will block here until the crawling is finished
