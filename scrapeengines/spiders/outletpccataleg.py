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


class OutletpcCataleg(scrapy.Spider):
    name = "outletpc_cataleg"
    #db = TinyDB('dbcataleg.json')
    #db = TinyDB('dbcataleg.json', storage=CachingMiddleware(JSONStorage))

    def start_requests_test(self):
         urls = [
            'https://outlet-pc.es/723-juegos-de-mesa?productListView=list&page=1&order=product.date_add.desc'
         ]
         for url in urls:
             yield scrapy.Request(url=url, callback=self.parse)

    def start_requests(self):

        urls = [
            'https://outlet-pc.es/723-juegos-de-mesa?productListView=list&page=1&order=product.date_add.desc'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        #page = response.url.split("/")[-2]
        #filename = 'quotes-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)
        
        for producteRAW in response.css('div.products-grid article.product-miniature'):

            hidden = producteRAW.css('a.delete').get()
            if hidden is None:
                loader = ItemLoader(item=Producte(), selector=producteRAW)
                loader.add_css('nom', 'h3.product-title > a::text')
                loader.add_css('url', 'h3.product-title > a::attr(href)')
                loader.add_css('preu', 'div.product-price-and-shipping span.product-price::text')
                loader.add_css('preu_original', 'div.product-price-and-shipping span.regular-price::text')

                agotado = producteRAW.css('div.producto_sin_stock').get()
                if agotado is None:
                    loader.add_value('stock','Disponible')
                else:
                    loader.add_value('stock','Agotado')

                producte = loader.load_item()

                producte['botiga']='Outletpc'



                yield producte


        
        #PAGINES SEGÜENTS
        for next_page in response.css('nav.pagination a[rel=next]::attr(href)'):
            #print("next!")
            yield response.follow(next_page, self.parse)
            pass
  

def outletpccatalog():
    print("fent catàleg...")

    process = CrawlerProcess(get_project_settings())
    process.crawl(OutletpcCataleg)
    process.start()  # the script will block here until the crawling is finished
