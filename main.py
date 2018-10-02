import requests
import xml.etree.ElementTree as ET
import sqlite3
import Utils


def categoryElementToBoolean(element):
    if element is not None:
        return True
    else:
        return False


conn = sqlite3.connect(':memory:')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

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

with open('getAllCategoriesCall.xml', 'r') as myfile:
    requestData = myfile.read()

response = requests.post(url, data=requestData, headers=headers).text
root = ET.fromstring(response)
inserts = []
for cat in root.findall('.//{urn:ebay:apis:eBLBaseComponents}Category'):
    id = cat.find('{urn:ebay:apis:eBLBaseComponents}CategoryID').text
    parentId = cat.find('{urn:ebay:apis:eBLBaseComponents}CategoryParentID').text
    level = cat.find('{urn:ebay:apis:eBLBaseComponents}CategoryLevel').text
    name = cat.find('{urn:ebay:apis:eBLBaseComponents}CategoryName').text
    autoPayEnabled = categoryElementToBoolean(cat.find('{urn:ebay:apis:eBLBaseComponents}AutoPayEnabled'))
    bestOfferEnabled = categoryElementToBoolean(cat.find('{urn:ebay:apis:eBLBaseComponents}BestOfferEnabled'))
    b2BVATEnabled = categoryElementToBoolean(cat.find('{urn:ebay:apis:eBLBaseComponents}B2BVATEnabled'))
    expired = categoryElementToBoolean(cat.find('{urn:ebay:apis:eBLBaseComponents}Expired'))
    leafCategory = categoryElementToBoolean(cat.find('{urn:ebay:apis:eBLBaseComponents}LeafCategory'))
    LSD = categoryElementToBoolean(cat.find('{urn:ebay:apis:eBLBaseComponents}LSD'))
    ORPA = categoryElementToBoolean(cat.find('{urn:ebay:apis:eBLBaseComponents}ORPA'))
    ORRA = categoryElementToBoolean(cat.find('{urn:ebay:apis:eBLBaseComponents}ORRA'))
    virtual = categoryElementToBoolean(cat.find('{urn:ebay:apis:eBLBaseComponents}Virtual'))

    inserts.append((id, parentId, level, name, autoPayEnabled, bestOfferEnabled, b2BVATEnabled, expired, leafCategory,
                    LSD, ORPA, ORRA, virtual))

cursor.execute('''CREATE TABLE IF NOT EXISTS categories
             (id INTEGER,
              parent_id INTEGER,
              level INTEGER,
              name TEXT,
              auto_pay_enabled INTEGER,
              best_offer_enabled INTEGER,
              b2b_enabled INTEGER,
              expired INTEGER,
              leaf_category INTEGER,
              LSD INTEGER,
              ORPA INTEGER,
              ORRA INTEGER,
              virtual INTEGER)''')
conn.commit()

cursor.executemany(
    '''INSERT INTO categories 
            (id,
            parent_id,
            level,
            name,
            auto_pay_enabled,
            best_offer_enabled,
            b2b_enabled,
            expired,
            leaf_category,
            LSD,
            ORPA,
            ORRA,
            virtual) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
    inserts)
conn.commit()

cursor.execute('SELECT * FROM categories')
forest = Utils.flatToTree(cursor.fetchall())
test = Utils.printTree(forest[0])
print(test)

conn.close()
print('finished')
