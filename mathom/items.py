# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst,Compose

def trimx(x):
    return x.strip()

def treu_moneda(x):
    return x.replace(' €', '')


class MathomItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
    
class Producte(scrapy.Item):
    nom = scrapy.Field( output_processor=TakeFirst())
    editorial = scrapy.Field( output_processor=TakeFirst())
    url = scrapy.Field( output_processor=TakeFirst())
    preu = scrapy.Field( output_processor=Compose(TakeFirst(),treu_moneda))
    preu_original = scrapy.Field( output_processor=Compose(TakeFirst(),treu_moneda))
    stock = scrapy.Field( output_processor=Compose(TakeFirst(),trimx))
    status = scrapy.Field()
    date_created = scrapy.Field(serializer=str)
    date_updated = scrapy.Field(serializer=str)


