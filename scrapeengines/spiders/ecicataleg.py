import scrapy
from scrapeengines.items import Producte
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class EciCataleg(scrapy.Spider):
    name = "eci_cataleg"

    def start_requests_test(self):
         urls = [
            'https://beta.elcorteingles.es/regalos-originales/juegos-de-entretenimiento/juegos-de-cartas/?sorting=discountPerDesc'
         ]
         for url in urls:
             yield scrapy.Request(url=url, callback=self.parse)

    def start_requests(self):

        urls = [
            'https://beta.elcorteingles.es/juguetes/juegos-de-mesa/estrategia/',
            'https://beta.elcorteingles.es/juguetes/juegos-de-mesa/estrategia/8/',
            'https://beta.elcorteingles.es/regalos-originales/juegos-de-entretenimiento/juegos-de-cartas/',
            'https://beta.elcorteingles.es/regalos-originales/juegos-de-entretenimiento/juegos-de-cartas/8/',
            'https://beta.elcorteingles.es/regalos-originales/juegos-de-entretenimiento/tableros/',
            'https://beta.elcorteingles.es/regalos-originales/juegos-de-entretenimiento/tableros/10/'

        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        #page = response.url.split("/")[-2]
       #filename = 'quotes-%s.html' % page
       # with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)
        
        for producteRAW in response.css('div#products-list div.product_preview-body'):

            loader = ItemLoader(item=Producte(), selector=producteRAW)
            loader.add_css('nom', 'div.title-box p.product_preview-desc::text')
            loader.add_css('url', 'div.title-box h2.plp_title_seo > a::attr(href)')
            loader.add_css('preu', 'div.product_preview-buy span.price')
            loader.add_css('preu_original', 'div.product_preview-buy span.price-tagline span.price')

            loader.add_value('stock','Disponible')

            producte = loader.load_item()

            producte['botiga']='ECI'



            yield producte


        
        #PAGINES SEGÜENTS
        for next_page in response.css('div.pagination a[rel=next]::attr(href)'):
            #print("next!")
            yield response.follow(next_page, self.parse)
            pass
  

def ecicatalog():
    print("fent catàleg...")

    process = CrawlerProcess(get_project_settings())
    process.crawl(EciCataleg)
    process.start()  # the script will block here until the crawling is finished
