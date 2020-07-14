# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import logging

from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from tinydb import TinyDB, Query
import pymongo
#from scrapy.conf import settings
from scrapeengines.avisos import Notificacions
from scrapeengines.avisos.Notificacions import Tipus_Notificacio,NotificacioService
from scrapeengines.items import Producte
from datetime import date

class MathomPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoDB(object):

    def __init__(self, mongo_server, mongo_db,mongo_port,mongo_collection,mongo_collection_avisos):
        self.mongo_server = mongo_server
        self.mongo_db = mongo_db
        self.mongo_port = mongo_port
        self.mongo_collection = mongo_collection
        self.mongo_collection_avisos = mongo_collection_avisos


    @classmethod
    def from_crawler(cls, crawler):
        ## pull in information from settings.py
        return cls(
            mongo_server=crawler.settings.get('MONGODB_SERVER'),
            mongo_db=crawler.settings.get('MONGODB_DB'),
            mongo_port=crawler.settings.get('MONGODB_PORT'),
            mongo_collection=crawler.settings.get('MONGODB_COLLECTION'),
            mongo_collection_avisos = crawler.settings.get('MONGODB_COLLECTION_AVISOS')
        )
    def open_spider(self, spider):
        self.mongoclient = pymongo.MongoClient(
            self.mongo_server,
            self.mongo_port
        )
        self.db = self.mongoclient.get_database(self.mongo_db).get_collection(self.mongo_collection)
        self.dbavisos = self.mongoclient.get_database(self.mongo_db).get_collection(self.mongo_collection_avisos)
        self.avisosService = NotificacioService()


    def process_item(self, producte, spider):

        Cerca = Query()

        results = self.db.find_one({"_id": producte['url'] })

        producteDB = results if results is not None else None

        logging.info("Producte: " + producte['nom'] + " @" + producte['botiga'])

        # print("Producte: "+ producte['nom'])

        if not producteDB:
            producte.init_new()
            #producte["_id"] = producte["url"]
            self.db.insert(dict(producte))
            notificacio = self.avisosService.nova_notificacio(Tipus_Notificacio.NOVETAT, producteDB, producte)
            self.dbavisos.insert(dict(notificacio.__dict__))

        else:
            if not "date_lastseen" in producteDB:
                producteDB['date_lastseen'] = '2000-01-01'
            if not "status_stock" in producteDB:
                producteDB['status_stock'] = ''
            if not "status_preu" in producteDB:
                producteDB['status_preu'] = ''
            if not "preu" in producte:
                producte['preu'] = 0
            if not "stock" in producte:
                producte['stock'] = "N/A"
            if producte['preu'] == '':
                producte['preu'] = 0
            if not producte.iguals(producteDB):
                # print ("Un diferent!")
                producteDB['date_lastseen'] = date.today().isoformat()

                if producteDB['stock'] == 'Agotado' and producte['stock'] == 'Disponible':
                    notificacio=self.avisosService.nova_notificacio(Tipus_Notificacio.RESTOCK, producteDB, producte)
                    self.dbavisos.insert(dict(notificacio.__dict__))
                    producteDB['status_stock'] = 'RESTOCK'
                    producteDB['stock'] = producte['stock']
                    producteDB['date_updated'] = date.today().isoformat()
                elif producteDB['stock'] == 'Disponible' and producte['stock'] == 'Agotado':
                    notificacio=self.avisosService.nova_notificacio(Tipus_Notificacio.ESGOTAT, producteDB, producte)
                    self.dbavisos.insert(dict(notificacio.__dict__))
                    producteDB['status_stock'] = 'ESGOTAT'
                    producteDB['stock'] = producte['stock']
                    producteDB['date_updated'] = date.today().isoformat()
                elif producteDB['status_stock'] == 'NOU':
                    notificacio=self.avisosService.nova_notificacio(Tipus_Notificacio.NOVETAT, producteDB, producte)
                    self.dbavisos.insert(dict(notificacio.__dict__))
                    producteDB['status_stock'] = 'STOCK'
                    producteDB['date_updated'] = date.today().isoformat()

                if float(producteDB['preu']) > float(producte['preu']):
                    if float(producte['preu']) > 0:
                        notificacio=self.avisosService.nova_notificacio(Tipus_Notificacio.REBAIXA, producteDB, producte)
                        self.dbavisos.insert(dict(notificacio.__dict__))
                    producteDB['status_preu'] = 'REBAIXAT'
                    producteDB['preu'] = float(producte['preu'])
                    producteDB['date_updated'] = date.today().isoformat()
                elif float(producteDB['preu']) < float(producte['preu']):
                    if float(producteDB['preu']) > 0:
                        notificacio=self.avisosService.nova_notificacio(Tipus_Notificacio.ENCAREIX, producteDB, producte)
                        self.dbavisos.insert(dict(notificacio.__dict__))
                    producteDB['status_preu'] = 'FIPROMO'
                    producteDB['preu'] = float(producte['preu'])
                    producteDB['date_updated'] = date.today().isoformat()
                elif producteDB['preu'] == producte['preu'] and producteDB['status_preu'] != "IGUAL":
                    producteDB['status_preu'] = 'IGUAL'
                    producteDB['date_updated'] = date.today().isoformat()

                self.db.update({'_id': producte['url']},dict(producteDB),upsert=True)


        return producte

    def close_spider(self, spider):
        self.mongoclient.close()
