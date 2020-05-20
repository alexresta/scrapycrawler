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


class ZacatrusCataleg(scrapy.Spider):
    name = "zacatrus_cataleg"
    #db = TinyDB('dbcataleg.json')
    #db = TinyDB('dbcataleg.json', storage=CachingMiddleware(JSONStorage))

    def start_requests_test(self):
         urls = [
            'https://zacatrus.es/juegos-de-mesa.html?p=250'
         ]
         for url in urls:
             yield scrapy.Request(url=url, callback=self.parse)

    def start_requests(self):

        urls = [
            'https://zacatrus.es/juegos-de-mesa.html?p=150&product_list_limit=36',
            'https://zacatrus.es/juegos-de-mesa.html?p=125&product_list_limit=36',
            'https://zacatrus.es/juegos-de-mesa.html?p=105&product_list_limit=36',
            'https://zacatrus.es/juegos-de-mesa.html?p=75&product_list_limit=36',
            'https://zacatrus.es/juegos-de-mesa.html?p=50&product_list_limit=36',
            'https://zacatrus.es/juegos-de-mesa.html?p=25&product_list_limit=36',
            'https://zacatrus.es/juegos-de-mesa.html?product_list_limit=36',
            'https://zacatrus.es/kilometro-0.html',
            'https://zacatrus.es/juegos-de-mesa.html?outlet2=1755&product_list_order=bestsellers'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
       # page = response.url.split("/")[-2]
        #filename = 'quotes-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)
        
        for producteRAW in response.css('li.product-item'):

            hidden = producteRAW.css('a.delete').get()
            if hidden is None:
                loader = ItemLoader(item=Producte(), selector=producteRAW)
                loader.add_css('nom', 'strong.product-item-name > a::text')
                loader.add_css('url', 'strong.product-item-name > a::attr(href)')
                loader.add_css('preu_original', 'div.price-box span[data-price-type=oldPrice] span.price::text')
                loader.add_css('preu', 'div.price-box span[data-price-type=finalPrice] span.price::text')

                unavailable = producteRAW.css('div.unavailable span').get()
                if unavailable is None:
                    loader.add_value('stock','Disponible')
                else:
                    loader.add_value('stock','Agotado')

                producte = loader.load_item()

                producte['botiga']='Zacatrus'



                yield producte


        
        #PAGINES SEGÜENTS
        for next_page in response.css('li.pages-item-next  a.next::attr(href)'):
            #print("next!")
            yield response.follow(next_page, self.parse)
            pass
  

def zacatrusfullcatalog():
    print("fent catàleg...")

    process = CrawlerProcess(get_project_settings())
    process.crawl(ZacatrusCataleg)
    process.start()  # the script will block here until the crawling is finished
