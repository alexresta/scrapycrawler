import scrapy
from scrapeengines.items import Producte
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class AtlanticaCataleg(scrapy.Spider):
    name = "atlantica_cataleg"

    def start_requests_test(self):
        urls = [
            'https://www.atlanticajuegos.com/es/8011071-serie-commands-colors'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def start_requests(self):

        urls = [
            'https://www.atlanticajuegos.com/es/3-juegos-de-mesa-por-marca?page=120',
            'https://www.atlanticajuegos.com/es/3-juegos-de-mesa-por-marca?page=90',
            'https://www.atlanticajuegos.com/es/3-juegos-de-mesa-por-marca?page=60',
            'https://www.atlanticajuegos.com/es/3-juegos-de-mesa-por-marca?page=30',
            'https://www.atlanticajuegos.com/es/3-juegos-de-mesa-por-marca',
            'https://www.atlanticajuegos.com/es/5-wargames?page=30',
            'https://www.atlanticajuegos.com/es/5-wargames'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #    f.write(response.body)
        # self.log('Saved file %s' % filename)
        for producteRAW in response.css('div.products article.product-miniature'):

            loader = ItemLoader(item=Producte(), selector=producteRAW)
            loader.add_css('nom', 'h3.product-title > a::text')
            loader.add_css('url', 'h3.product-title > a::attr(href)')
            loader.add_css('preu', 'div.product-price-and-shipping span.price span:nth-child(2)::text')
            loader.add_css('preu_original', 'div.product-price-and-shipping span.regular-price::text')

            # agotado = producteRAW.css('ul.product-flags li.agotado').get()

            loader.add_value('stock', 'Disponible')

            producte = loader.load_item()

            producte['botiga'] = 'Atlantica'

            yield producte

        # PAGINES SEGÜENTS
        for next_page in response.css('ul.page-list a[rel=next]::attr(href)'):
            # print("next!")
            yield response.follow(next_page, self.parse)
            # pass


def atlanticafullcatalog():
    print("fent catàleg...")

    process = CrawlerProcess(get_project_settings())
    process.crawl(AtlanticaCataleg)
    process.start()  # the script will block here until the crawling is finished
