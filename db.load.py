import yaml
import db_connection as db_con
import json
import pandas as pd

conn = db_con.connect_to_db(config_file='config.yaml', section='mongo_azure_mooc', ssh=False, local_port=None, ssh_section= 'ssh_tunnel')

# Get a reference to the collection you want to read
collection = conn["MOOC_forum"]

# Read the documents in the collection
documents = collection.find().limit(1)

# Iterate over the documents and print their contents
for doc in documents:
    json_formatted_str = json.dumps(doc, indent=2)
    print(json_formatted_str)



def nombre_messages(documents):
    cumul = 1
    print(f"id: {documents['id']}")
    for message in documents['children']:
        cumul = nombre_messages(message)
    print(f"id: {documents["id"]} : ")


# with open('sample.json') as f:
#     for line in f:
#         # print(line)
#         x=json.loads(line)
#         print(x)