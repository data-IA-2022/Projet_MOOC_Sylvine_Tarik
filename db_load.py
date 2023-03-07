import yaml, utils
import db_connection as db_con
import json
import pandas as pd
from sqlalchemy import text, create_engine
from pymongo import MongoClient
import time

## I. Connexion aux BDD 
# Connexion à mongodb
conn = db_con.connect_to_db(config_file='config.yaml', section='mongo_datalab', ssh=False, local_port=None, ssh_section= 'ssh_tunnel_datalab')
# Connexion à mysql
# conn_mysql_datalab = db_con.connect_to_db(config_file='config.yaml', section='mysql_datalab', ssh=False, local_port=None, ssh_section= 'ssh_tunnel_datalab')

# Version Sylvine:
# mysql = "mysql://root:greta2023@127.0.0.1/g5"
mysql = "mysql://root:greta2023@127.0.0.1/g5_sylvine"
conn_mysql_datalab = create_engine(mysql)

print('---------------------------')
print(f"connexion Mongo : {conn}")
print(f"connexion SQL : {conn_mysql_datalab}")
print('---------------------------')



# Get a reference to the collection you want to read
forum_collection = conn["forum"]
user_collection = conn["user"]

# doc = forum_collection.find_one({"_id": "52ef50b5cfc81d7e4100090e"})
# print(doc)
# print(type(doc))
# quit()

doc = user_collection.find_one({"username": "Ego41"})
print(doc)
print(type(doc))
quit()

cursor = forum_collection.find(filter=None, projection={'annotated_content_info': 0, '_id': 1})#.limit(5000)
nbre_docs = cursor.count()
print('nbre de doc: ', nbre_docs)

quit()

# # Création de la database en sql avec sqlalchemy



# result = conn_mysql_datalab.execute("SHOW TABLES;")
# tables = result.fetchall()
# print(tables)



# quit()


def traitement(msg, parent_id=None, thread_id=None):
    '''
    Effectue un traitement sur l'obj passé (Message)
    :param msg: Message
    :return:
    '''
    
    username = msg['username'] if 'username' in msg else None
    dt = msg['created_at']
    dt = dt[:10]+' '+dt[11:19]
    thread_id = msg['id']
    body_length = len(msg['body'])
    print("Recurse ", msg['id'], msg['depth'] if 'depth' in msg else '-', parent_id, dt, thread_id)
    if len(msg['body'])>65000:
        #print(msg['body'])
        msg['body'] = msg['body'][:65000]
    
    if not msg['anonymous'] and 'username' in msg:
        conn_mysql_datalab.execute("INSERT IGNORE INTO Users (username, user_id) VALUES (%s,%s) ;", [msg['username'], msg['user_id']])
    conn_mysql_datalab.execute("""INSERT INTO Messages 
                        (id, type, created_at, username, depth, thread_id, body, parent_id, body_length) 
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE parent_id=VALUES(parent_id), depth=VALUES(depth);""",
                        [msg['id'], msg['type'], dt, username, msg['depth'] if 'depth' in msg else None, thread_id, msg['body'], parent_id, body_length])

# # Solution sans en être une pour palier à l'erreur sqlalchemy.exc.IntegrityError sur la FK thread_id dans la table message
# conn_mysql_datalab.execute("SET FOREIGN_KEY_CHECKS=0;")
for doc in cursor:
    #print(doc)
    starting_time = time.time()
    
    print('-------------------------------------------------------------------------')
    #print(json.dumps(doc, indent=4))
    print(doc['_id'], doc['content']['course_id'])
    try:
        dt =  doc['content']['created_at']
        dt = dt[:10]
        
        conn_mysql_datalab.execute("INSERT IGNORE INTO Mooc (course_id, opening_date) VALUES (%s,%s) ;", [doc['content']['course_id'], dt])
        conn_mysql_datalab.execute("INSERT IGNORE INTO Threads (_id,course_id) VALUES (%s,%s) ;", [doc['_id'], doc['content']['course_id']])
        
        utils.recur_message(doc['content'], traitement,  doc['_id'])
    except ValueError:
        print(ValueError)
        quit()
 
# conn_mysql_datalab.execute("SET FOREIGN_KEY_CHECKS=1;")   
duree = time.time() - starting_time
print(f"durée de chargement des tables Messages, Mooc, Threads, Users: {int(duree/3600)} H {int(duree%3600/60)} M {duree%3600%60}")

# # quit()

########################################## Insertion de la table Results ############################
# Execute the query
cursor2 = user_collection.find()#.limit(1)
nbre_docs = cursor2.count()
print('nbre de doc: ', nbre_docs)

# Print the results
for document in cursor2:
    starting_time = time.time()
    keys = [k for k in document.keys() if k not in ['_id', 'id', 'username']]
    username = document["username"]
    # print(username)
    print('-------------------------------------------------------------------------')
    for course_id in keys:
        # print(course )
        sub_doc = document[course_id]
        if sub_doc.get("grade") in sub_doc:
            grade = sub_doc.get("grade")
            certificate_eligible = sub_doc.get("Certificate Eligible")
            gender = sub_doc.get("gender") if 'gender' in sub_doc else ''
            if gender=='None': gender=''
            country=sub_doc.get("country") if 'country' in sub_doc else ''
            level_of_education=sub_doc.get("level_of_education") if 'level_of_education' in sub_doc else ''
            conn_mysql_datalab.execute("""INSERT INTO Users (username, country, gender, level_of_education) 
                                VALUES (%s,%s,%s,%s) 
                                ON DUPLICATE KEY UPDATE country=VALUES(country), gender=VALUES(gender), level_of_education=VALUES(level_of_education);""",
                                [username, country, gender, level_of_education])
            print("Update dans Users", username, country, gender, level_of_education)
            conn_mysql_datalab.execute("INSERT IGNORE INTO Results (course_id, username, grade, certificate_eligible) VALUES (%s,%s,%s,%s) ;", [course_id, username, grade, certificate_eligible])
            conn_mysql_datalab.execute("""INSERT INTO Mooc (course_id) 
                                VALUES (%s)
                                ON DUPLICATE KEY UPDATE course_id=VALUES(course_id);""", [course_id])
            print("Insertion dans Results",course_id, username, grade, certificate_eligible)

duree = time.time() - starting_time
print(f"durée de chargement table Results {int(duree/3600)} H {int(duree%3600/60)} M {duree%3600%60}")




# for doc in cursor2:
    

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



# # Read the documents in the collection
# documents = forum_collection.find().limit(1)

# # Iterate over the documents and print their contents
# for doc in documents:
#     json_formatted_str = json.dumps(doc, indent=2)
#     print(json_formatted_str)



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

# conn_mysql_datalab = db_con.connect_to_db(config_file='config.yaml', section='mysql_datalab', ssh=False, local_port=None, ssh_section= 'ssh_tunnel_datalab')


# # Création de la database en sql avec sqlalchemy

# from sqlalchemy import text

# result = conn_mysql_datalab.execute(text('SHOW TABLES;'))
# tables = result.fetchall()
# print(tables)
