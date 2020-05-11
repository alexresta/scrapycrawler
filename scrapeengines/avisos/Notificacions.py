from tinydb import TinyDB, Query, JSONStorage
from datetime import date
from enum import Enum

from tinydb.middlewares import CachingMiddleware


class Tipus_Notificacio(str,Enum):
    REBAIXA = "REBAIXA"
    RESTOCK = "RESTOCK"
    ESGOTAT = "ESGOTAT"
    NOVETAT = "NOVETAT"
    DESCATALOGAT = "DESCATALOGAT"
    ENCAREIX = "ENCAREIX"


class Notificacio:
    tipus_notificacio = None
    preu_anterior = ""
    preu_actual = ""
    producte = ""
    botiga = ""
    url = ""
    data = ""

    def __init__(self, tipus_notificacio, preu_anterior, producte):
        self.tipus_notificacio = tipus_notificacio
        self.preu_anterior = preu_anterior
        self.preu_actual = producte['preu']
        self.producte = producte['nom']
        self.botiga = producte['botiga']
        self.url = producte['url']
        self.data = date.today().isoformat()

class NotificacioService:

    def dbopen(self):
        self.dbavisos = TinyDB('dbavisos.json', storage=CachingMiddleware(JSONStorage))

    def dbclose(self):
        self.dbavisos.close()


    def nova_notificacio(self,tipus_notificacio, producteBD, producte):
        preu_antic = producte['preu'];

        if producteBD:
            preu_antic = producteBD['preu']

        notificacio = Notificacio(tipus_notificacio, preu_antic, producte)

        self.dbavisos.insert(notificacio.__dict__)
