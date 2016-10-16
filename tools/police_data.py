from lxml import html
from lxml.html.clean import Cleaner
import requests

class PoliceStationModel(object):
    ID = "_id"
    NAME = "name"
    ADDRESS = "address"
    LAT = "lat"
    LONG = "long"

    def __init__(self):

        self.id = None
        self.name = None
        self.address = None
        self.lat = None
        self.long = None

    def toDict(self):
        """

        :return:
        """

        dictModel = dict()

        dictModel[self.ID] = self.id
        dictModel[self.NAME] = self.name
        dictModel[self.ADDRESS] = self.address
        dictModel[self.LAT] = self.lat
        dictModel[self.LONG] = self.long

        return dictModel

    @classmethod
    def fromDict(cls, dictModel):
        """

        :return:
        """

        model = PoliceStationModel()
        model.id = dictModel.get(cls.ID)
        model.name = dictModel.get(cls.NAME)
        model.address = dictModel.get(cls.ADDRESS)
        model.lat = dictModel.get(cls.LAT)
        model.long = dictModel.get(cls.LONG)

        return model

[{"name" : "Sectia 1 Politie", "address" : "Bld. Lascar Catargiu nr. 22, sector 1", "lat" : 44.491765, "long" : 26.048768},
{"name" : "Sectia 2 Politie", "address" : "Str. Promoroacă nr. 10, sector 1", "lat" : 44.490958, "long" : 26.087876},
{"name" : "Sectia 3 Politie", "address" : "Str. Gral Mathias Berthelot nr.34, sector 1", "lat" : 44.491765, "long" : 26.048768},
{"name" : "Sectia 4 Politie", "address" : "Str. Ion Neculce nr.6, sectorul 1", "lat" : 44.455728, "long" : 26.072592},
{"name" : "Sectia 5 Politie", "address" : "Bd. Bucureştii Noi nr. 54, sectorul 1", "lat" : 44.482567, "long" : 26.041229}]


# session = requests.session()
# cleaner = Cleaner()

# def GetPageData(url) :
#     resp = session.get(url)
#
#     if resp.status_code != 200:
#         print("Error at url %s. Content: %s" % (url, resp.content))
#         return
#
#     content = resp.content
#     html_start = content.find("<!DOCTYPE".encode('utf-8'))
#     content = content[html_start:]
#     content = cleaner.clean_html(content)
#
#     with open("data.html", "w") as f:
#         f.write(str(content))
#     return parse_page(content)
#
# def parse_page(content):
#
#     tree = html.document_fromstring(content)
#     nodes = tree.find_class('boxStire')
#     objects = list()
#
#     for divEl in nodes:
#
#         obj = PoliceStationModel()
#         obj.name = divEl.find_class('openBold')[0].attrib['title']
#
#         addressDiv = divEl.find_class('boxStireDesc')
#
#         for pElem in addressDiv[0].getchildren():
#
#             for pChild in pElem.getchildren():
#                 if pChild.tag == 'span' and pChild.getchildren() and 'Adresa' in pChild.getchildren()[0].text:
#                     if pChild.getchildren()[0].tail:
#                         obj.address = pChild.getchildren()[0].tail
#                 elif pChild.tag == 'strong' and pChild.getchildren() and 'Adresa' in pChild.getchildren()[0].text:
#                     obj.address = pChild.getchildren[1].text
#
#                 break
#         objects.append(obj);
#
#     return objects;
#
#
# #https://b.politiaromana.ro/ro/structura/politia-sectorului-1
# GetPageData('https://b.politiaromana.ro/ro/structura/politia-sectorului-1')




















