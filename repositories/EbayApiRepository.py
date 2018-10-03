import requests
import xml.etree.ElementTree as ET
from utils import Utils


def getAllCategoriesAsText():
    url = 'https://api.sandbox.ebay.com/ws/api.dll'

    headers = {
        'X-EBAY-API-CALL-NAME': 'GetCategories',
        'X-EBAY-API-APP-NAME': 'EchoBay62-5538-466c-b43b-662768d6841',
        'X-EBAY-API-CERT-NAME': '00dd08ab-2082-4e3c-9518-5f4298f296db',
        'X-EBAY-API-DEV-NAME': '16a26b1b-26cf-442d-906d-597b60c41c19',
        'X-EBAY-API-SITEID': 0,
        'X-EBAY-API-COMPATIBILITY-LEVEL': 861,
        'Content-Type': 'text/xml'
    }

    with open('resources/getAllCategoriesCall.xml', 'r') as myfile:
        requestData = myfile.read()

    return requests.post(url, data=requestData, headers=headers).text


def categoriesXmlToListOfTouples(categoriesAsText):
    root = ET.fromstring(categoriesAsText)
    inserts = []
    for cat in root.findall('.//{urn:ebay:apis:eBLBaseComponents}Category'):
        id = cat.find('{urn:ebay:apis:eBLBaseComponents}CategoryID').text
        parentId = cat.find('{urn:ebay:apis:eBLBaseComponents}CategoryParentID').text
        level = cat.find('{urn:ebay:apis:eBLBaseComponents}CategoryLevel').text
        name = cat.find('{urn:ebay:apis:eBLBaseComponents}CategoryName').text
        autoPayEnabled = Utils.categoryElementToBoolean(cat.find('{urn:ebay:apis:eBLBaseComponents}AutoPayEnabled'))
        bestOfferEnabled = Utils.categoryElementToBoolean(cat.find('{urn:ebay:apis:eBLBaseComponents}BestOfferEnabled'))
        b2BVATEnabled = Utils.categoryElementToBoolean(cat.find('{urn:ebay:apis:eBLBaseComponents}B2BVATEnabled'))
        expired = Utils.categoryElementToBoolean(cat.find('{urn:ebay:apis:eBLBaseComponents}Expired'))
        leafCategory = Utils.categoryElementToBoolean(cat.find('{urn:ebay:apis:eBLBaseComponents}LeafCategory'))
        LSD = Utils.categoryElementToBoolean(cat.find('{urn:ebay:apis:eBLBaseComponents}LSD'))
        ORPA = Utils.categoryElementToBoolean(cat.find('{urn:ebay:apis:eBLBaseComponents}ORPA'))
        ORRA = Utils.categoryElementToBoolean(cat.find('{urn:ebay:apis:eBLBaseComponents}ORRA'))
        virtual = Utils.categoryElementToBoolean(cat.find('{urn:ebay:apis:eBLBaseComponents}Virtual'))

        inserts.append(
            (id, parentId, level, name, autoPayEnabled, bestOfferEnabled, b2BVATEnabled, expired, leafCategory,
             LSD, ORPA, ORRA, virtual))

    return inserts
