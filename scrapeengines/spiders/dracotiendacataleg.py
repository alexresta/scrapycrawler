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


class DracotiendaCataleg(scrapy.Spider):
    name = "dracotienda_cataleg"
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
            'https://dracotienda.com/1715-juegos-de-tablero?page=175',
            'https://dracotienda.com/1729-juegos-de-cartas?page=100',
            'https://dracotienda.com/1715-juegos-de-tablero?page=150',
            'https://dracotienda.com/1776-wargames?page=50',
            'https://dracotienda.com/1715-juegos-de-tablero?page=125',
            'https://dracotienda.com/1729-juegos-de-cartas?page=75',
            'https://dracotienda.com/1776-wargames?page=25',
            'https://dracotienda.com/1715-juegos-de-tablero?page=100',
            'https://dracotienda.com/1729-juegos-de-cartas?page=50',
            'https://dracotienda.com/1776-wargames',
            'https://dracotienda.com/1715-juegos-de-tablero?page=75',
            'https://dracotienda.com/1729-juegos-de-cartas?page=25',
            'https://dracotienda.com/1715-juegos-de-tablero?page=50',
            'https://dracotienda.com/1729-juegos-de-cartas',
            'https://dracotienda.com/1715-juegos-de-tablero?page=25',
            'https://dracotienda.com/1879-ofertas',
            'https://dracotienda.com/1715-juegos-de-tablero',
            'https://dracotienda.com/1796-juegos-infantiles'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
       # page = response.url.split("/")[-2]
        #filename = 'quotes-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)
        for producteRAW in response.css('div.laberProductGrid div.item'):


            loader = ItemLoader(item=Producte(), selector=producteRAW)
            loader.add_css('nom', 'h2.productName > a::text')
            loader.add_css('url', 'h2.productName > a::attr(href)')
            loader.add_css('preu', 'div.laber-product-price-and-shipping span.price::text')
            loader.add_css('preu_original', 'div.laber-product-price-and-shipping span.regular-price::text')

            available = producteRAW.css('div.LaberProduct-availability span.product-availability').get()
            if "Fuera de stock" in available:
                loader.add_value('stock','Agotado')
            else:
                loader.add_value('stock','Disponible')

            producte = loader.load_item()

            producte['botiga']='Dracotienda'

            yield producte


        
        #PAGINES SEGÜENTS
        for next_page in response.css('nav.pagination a[rel=next]::attr(href)'):
            #print("next!")
            yield response.follow(next_page, self.parse)
            #pass
  

def dracotiendafullcatalog():
    print("fent catàleg...")

    process = CrawlerProcess(get_project_settings())
    process.crawl(DracotiendaCataleg)
    process.start()  # the script will block here until the crawling is finished
