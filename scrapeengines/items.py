# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst,Compose
from datetime import date

from w3lib.html import remove_tags


def trimx(x):
    return x.strip()

def neteja_moneda(x):
    replaced =  x.replace(' €', '')
    replaced =  replaced.replace(' €', '')
    replaced =  replaced.replace(',', '.')

    return replaced

def neteja_caracters(x):
    replaced =  x.replace('&Amp;', '\u0026')
    replaced =  replaced.replace('\n', '')

    return replaced


class MathomItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
    
class Producte(scrapy.Item):
    nom = scrapy.Field( output_processor=Compose(TakeFirst(),neteja_caracters,trimx))
    editorial = scrapy.Field( output_processor=TakeFirst())
    url = scrapy.Field( output_processor=TakeFirst())
    preu = scrapy.Field( output_processor=Compose(TakeFirst(),remove_tags,neteja_moneda))
    preu_original = scrapy.Field( output_processor=Compose(TakeFirst(),remove_tags,neteja_moneda))
    stock = scrapy.Field( output_processor=Compose(TakeFirst(),trimx))
    status_stock = scrapy.Field()
    status_preu = scrapy.Field()
    date_lastseen = scrapy.Field(serializer=str)
    date_created = scrapy.Field(serializer=str)
    date_updated = scrapy.Field(serializer=str)
    botiga = scrapy.Field(serializer=str)
    _id = scrapy.Field(serializer=str)

    def test(self):
        return self['nom']

    def init_new(self):
        self['date_created'] = date.today().isoformat()
        self['date_lastseen'] = date.today().isoformat()
        self['status_stock'] = 'NOU'
        self['status_preu'] = 'IGUAL'
        if not "preu" in self:
            self['preu'] = 0
        else:
            if self['preu'] != '':
                self['preu'] = float(self['preu'])

        if "preu_original" in self:
            self['preu_original'] = float(self['preu_original'])
        else:
            self['preu'] = float(self['preu'])
        if not "stock" in self:
            self['stock'] = "N/A"
        self['_id'] = self['url']

    def iguals(self, producteDB):

        if all ([self['preu'] == producteDB['preu'], self['stock'] == producteDB['stock'],  producteDB['date_lastseen'] == date.today().isoformat()]):
            return True
        else:
            return False

