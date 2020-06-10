import sys
import time

from multiprocessing import Process
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scrapeengines.spiders.dracotiendacataleg import DracotiendaCataleg
from scrapeengines.spiders.egdgamescataleg import EgdgamesCataleg
from scrapeengines.spiders.jugamosotracataleg import JugamosotraCataleg
from scrapeengines.spiders.mathomcataleg import MathomCataleg
from scrapeengines.spiders.jugamosunacataleg import JugamosunaCataleg
from scrapeengines.spiders.outletpccataleg import OutletpcCataleg
from scrapeengines.spiders.zacatruscataleg import ZacatrusCataleg
from scrapeengines.spiders.juguetestoday import JuguetestodayCataleg


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

def dracotiendafullcatalog():

    process = CrawlerProcess(get_project_settings())
    process.crawl(DracotiendaCataleg)
    process.start()  # the script will block here until the crawling is finished

def jugamosotrafullcatalog():

    process = CrawlerProcess(get_project_settings())
    process.crawl(JugamosotraCataleg)
    process.start()  # the script will block here until the crawling is finished

def outletpcfullcatalog():

    process = CrawlerProcess(get_project_settings())
    process.crawl(OutletpcCataleg)
    process.start()  # the script will block here until the crawling is finished

def juguetestodayfullcatalog():

    process = CrawlerProcess(get_project_settings())
    process.crawl(JuguetestodayCataleg)
    process.start()  # the script will block here until the crawling is finished


def allparallel():
    process = CrawlerProcess(get_project_settings())
    process.crawl(MathomCataleg)
    process.crawl(JugamosunaCataleg)
    process.crawl(EgdgamesCataleg)
    process.crawl(ZacatrusCataleg)
    process.crawl(DracotiendaCataleg)
    process.crawl(JugamosotraCataleg)
    process.crawl(OutletpcCataleg)
    process.crawl(JuguetestodayCataleg)

    process.start()

if __name__ == "__main__":
    if sys.argv[1] == 'mathomcataleg':
        mathomcataleg()
    elif sys.argv[1] == 'jugamosunacataleg':
        jugamosunacataleg()
    elif sys.argv[1] == 'egdgamescataleg':
        egdgamesfullcatalog()
    elif sys.argv[1] == 'zacatruscataleg':
        zacatrusfullcatalog()
    elif sys.argv[1] == 'dracotiendacataleg':
        dracotiendafullcatalog()
    elif sys.argv[1] == 'jugamosotracataleg':
        jugamosotrafullcatalog()
    elif sys.argv[1] == 'outletpccataleg':
        outletpcfullcatalog()
    elif sys.argv[1] == 'juguetestodaycataleg':
        juguetestodayfullcatalog()
    elif sys.argv[1] == 'allparallel':
        allparallel()
    else:
        print("not found")