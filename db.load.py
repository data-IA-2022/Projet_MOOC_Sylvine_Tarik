import yaml
import db_connection as db_con
import json
import pandas as pd
from sqlalchemy import text



conn = db_con.connect_to_db(config_file='config.yaml', section='mongo_datalab', ssh=True, local_port=None, ssh_section= 'ssh_tunnel_datalab')

# Get a reference to the collection you want to read
forum_collection = conn["forum"]
user_collection = conn["user"]


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
