import sys

from multiprocessing import Process
from scrapy.crawler import CrawlerProcess
from scrapeengines.spiders.mathomofertes import MathomOfertes
from scrapy.utils.project import get_project_settings
from scrapeengines.spiders.mathomcataleg import MathomCataleg
from scrapeengines.spiders.jugamosunacataleg import JugamosunaCataleg


def mathomofertes():
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'items.json'
    })

    process.crawl(MathomOfertes)
    process.start()  # the script will block here until the crawling is finished


def mathomcataleg():

    process = CrawlerProcess(get_project_settings())
    process.crawl(MathomCataleg)
    process.start()  # the script will block here until the crawling is finished

def jugamosunacataleg():

    process = CrawlerProcess(get_project_settings())
    process.crawl(JugamosunaCataleg)
    process.start()  # the script will block here until the crawling is finished




if __name__ == "__main__":
    if sys.argv[1] == 'ofertesmathom':
        mathomofertes()
    elif sys.argv[1] == 'mathomcataleg':
        mathomcataleg()
    elif sys.argv[1] == 'jugamosunacataleg':
        jugamosunacataleg()
    else:
        print("not found")