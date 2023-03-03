import yaml, utils
import db_connection as db_con
import json
import pandas as pd
from sqlalchemy import text
from pymongo import MongoClient


# Connexion à mongodb
conn = db_con.connect_to_db(config_file='config.yaml', section='mongo_datalab', ssh=False, local_port=None, ssh_section= 'ssh_tunnel_datalab')
# Connexion à mysql
conn_mysql_datalab = db_con.connect_to_db(config_file='config.yaml', section='mysql_datalab', ssh=False, local_port=None, ssh_section= 'ssh_tunnel_datalab')



# Get a reference to the collection you want to read
forum_collection = conn["forum"]
user_collection = conn["user"]

# doc = forum_collection.find_one({"_id": "52ef50b5cfc81d7e4100090e"})
# print(doc)
# quit()
cursor = forum_collection.find(filter=None, projection={'annotated_content_info': 0, '_id': 1}).limit(5000)
nbre_docs = cursor.count()
print('nbre de doc: ', nbre_docs)

# quit()


def traitement(msg, parent_id=None):
    '''
    Effectue un traitement sur l'obj passé (Message)
    :param msg: Message
    :return:
    '''
    username = msg['username'] if 'username' in msg else None
    dt = msg['created_at']
    dt = dt[:10]+' '+dt[11:19]
    print("Recurse ", msg['id'], msg['depth'] if 'depth' in msg else '-', parent_id, dt)

    if not msg['anonymous']:
        conn_mysql_datalab.execute("INSERT IGNORE INTO Users (username, user_id) VALUES (%s,%s) ;", [msg['username'], msg['user_id']])
    conn_mysql_datalab.execute("""INSERT INTO Messages 
                        (id, type, created_at, username, depth, body, parent_id) 
                        VALUES (%s,%s,%s,%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE parent_id=VALUES(parent_id), depth=VALUES(depth);""",
                        [msg['id'], msg['type'], dt, username, msg['depth'] if 'depth' in msg else None, msg['body'], parent_id])


for doc in cursor:
    #print(doc)
    print('-------------------------------------------------------------------------')
    #print(json.dumps(doc, indent=4))
    print(doc['_id'], doc['content']['course_id'])

    conn_mysql_datalab.execute("INSERT IGNORE INTO Mooc (course_id) VALUES (%s) ;", [doc['content']['course_id']])
    conn_mysql_datalab.execute("INSERT IGNORE INTO Threads (_id,course_id) VALUES (%s,%s) ;", [doc['_id'], doc['content']['course_id']])

    utils.recur_message(doc['content'], traitement)

quit()


# # Loading or Opening the json file
# with open('C:\\Users\\tarik\\OneDrive\\Documents\\Formation_Dév_IA\\Projet_MOOC\\MOOC\\MOOC_forum.json', encoding='utf-8') as file:
#     file_data = json.load(file)


# # Inserting the loaded data in the Collection
# # if JSON contains data more than one entry
# # insert_many is used else insert_one is used
# if isinstance(file_data, list):
#     forum_collection.insert_many(file_data) 
# else:
#     forum_collection.insert_one(file_data)



# Read the documents in the collection
documents = forum_collection.find().limit(1)

# Iterate over the documents and print their contents
for doc in documents:
    json_formatted_str = json.dumps(doc, indent=2)
    print(json_formatted_str)



# # Etape 4 : Compter le nombre de messages par utilisateur
# pipeline = [
#         {"$unwind": "$content"},
#         {"$group": {"_id": "$content.username", "count": {"$sum": 1}}}
# ]

# result = list(forum_collection.aggregate(pipeline))
# print(f"{len(result)} utilisateurs ont posté des messages")

# # def nombre_messages(documents):
# #     cumul = 1
# #     print(f"id: {documents['id']}")
# #     for message in documents['children']:
# #         cumul = nombre_messages(message)
# #     print(f"id: {documents["id"]} : ")


# # with open('sample.json') as f:
# #     for line in f:
# #         # print(line)
# #         x=json.loads(line)
# #         print(x)


# #Create mysql db on Datalab

# # Connection à la db

conn_mysql_datalab = db_con.connect_to_db(config_file='config.yaml', section='mysql_datalab', ssh=False, local_port=None, ssh_section= 'ssh_tunnel_datalab')


# # Création de la database en sql avec sqlalchemy

from sqlalchemy import text

result = conn_mysql_datalab.execute(text('SHOW TABLES;'))
tables = result.fetchall()
print(tables)
