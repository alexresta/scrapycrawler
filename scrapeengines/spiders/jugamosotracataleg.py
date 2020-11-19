import scrapy
from scrapeengines.items import Producte
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class JugamosotraCataleg(scrapy.Spider):
    name = "jugamosotra_cataleg"

    def start_requests_test(self):
         urls = [
            'https://jugamosotra.com/24-juegos?page=20'
         ]
         for url in urls:
             yield scrapy.Request(url=url, callback=self.parse)

    def start_requests(self):

        urls = [
            'https://jugamosotra.com/24-juegos?page=20',
            'https://jugamosotra.com/24-juegos?page=15',
            'https://jugamosotra.com/24-juegos?page=10',
            'https://jugamosotra.com/24-juegos?page=5',
            'https://jugamosotra.com/24-juegos'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
       # page = response.url.split("/")[-2]
        #filename = 'quotes-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)
        for producteRAW in response.css('div.products article.product-miniature'):


            loader = ItemLoader(item=Producte(), selector=producteRAW)
            loader.add_css('nom', 'h2.product-title > a::text')
            loader.add_css('url', 'h2.product-title > a::attr(href)')
            loader.add_css('preu', 'div.product-price-and-shipping span.price::text')
            loader.add_css('preu_original', 'div.product-price-and-shipping span.regular-price::text')

            agotado = producteRAW.css('ul.product-flags li.agotado').get()
            if agotado is not None:
                loader.add_value('stock','Agotado')
            else:
                loader.add_value('stock','Disponible')

            producte = loader.load_item()

            producte['botiga']='Jugamosotra'

            yield producte


        
        #PAGINES SEGÜENTS
        for next_page in response.css('ul.page-list a[rel=next]::attr(href)'):
            #print("next!")
            yield response.follow(next_page, self.parse)
            #pass
  

def jugamosotrafullcatalog():
    print("fent catàleg...")

    process = CrawlerProcess(get_project_settings())
    process.crawl(JugamosotraCataleg)
    process.start()  # the script will block here until the crawling is finished
