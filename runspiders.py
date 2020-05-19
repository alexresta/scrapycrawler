import sys

from multiprocessing import Process
from scrapy.crawler import CrawlerProcess

from scrapeengines.spiders.egdgamescataleg import EgdgamesCataleg
from scrapeengines.spiders.mathomofertes import MathomOfertes
from scrapy.utils.project import get_project_settings
from scrapeengines.spiders.mathomcataleg import MathomCataleg
from scrapeengines.spiders.jugamosunacataleg import JugamosunaCataleg
from scrapeengines.spiders.zacatruscataleg import ZacatrusCataleg


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

def egdgamesfullcatalog():

    process = CrawlerProcess(get_project_settings())
    process.crawl(EgdgamesCataleg)
    process.start()  # the script will block here until the crawling is finished

def zacatrusfullcatalog():

    process = CrawlerProcess(get_project_settings())
    process.crawl(ZacatrusCataleg)
    process.start()  # the script will block here until the crawling is finished


if __name__ == "__main__":
    if sys.argv[1] == 'mathomcataleg':
        mathomcataleg()
    elif sys.argv[1] == 'jugamosunacataleg':
        jugamosunacataleg()
    elif sys.argv[1] == 'egdgamescataleg':
        egdgamesfullcatalog()
    elif sys.argv[1] == 'zacatruscataleg':
        zacatrusfullcatalog()
    else:
        print("not found")