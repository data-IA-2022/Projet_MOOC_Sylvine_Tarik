#import librairie
import json, utils
from pymongo import MongoClient

# connection (Attention : tunnel 27017)
# faire le tunnel avant
#url = 'mongodb://172.17.0.2:27017' # si sur VM
url = 'mongodb://127.0.0.1:27017' # si tunnel
client = MongoClient(url)
col = client.MOOC.forum #BD

print(f"col = {col}")

for doc in col.find():
    print(doc)
    try:
        utils.nombre_messages(doc['content'])
    catch Exception :
        print(json.loads(doc, indent = 4))
        quit()



# # utilisation de la BDD / collection
# db = client['DB_name']
# col = db['Collec_name']
# col = client.testEG.MOOC # BD testEG, collec MOOC

# insertion d’un document
# doc = {'x' : 10, 'y' : 99}
# collec.insert_one(doc)