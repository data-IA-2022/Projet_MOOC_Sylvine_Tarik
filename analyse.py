import db_connection as db_con
import json
import pandas as pd

# For ploting graph / Visualization
import plotly.express as px
from plotly.offline import iplot

# notion importante pour plotly il faut lui dire dans quel env il doit afficher les graphiques
# Default_renderer: 'browser'
# Available renderers:
#     ['plotly_mimetype', 'jupyterlab', 'nteract', 'vscode',
#      'notebook', 'notebook_connected', 'kaggle', 'azure', 'colab',
#      'cocalc', 'databricks', 'json', 'png', 'jpeg', 'jpg', 'svg',
#      'pdf', 'browser', 'firefox', 'chrome', 'chromium', 'iframe',
#      'iframe_connected', 'sphinx_gallery', 'sphinx_gallery_png']
# io.renderers.default = "notebook_connected"


# Connexion à mongodb
conn = db_con.connect_to_db(config_file='config.yaml', section='mongo_datalab', ssh=False, local_port=None, ssh_section= 'ssh_tunnel_datalab')
# Connexion à mysql
conn_mysql_datalab = db_con.connect_to_db(config_file='config.yaml', section='mysql_datalab', ssh=False, local_port=None, ssh_section= 'ssh_tunnel_datalab')


# Get a reference to the collection you want to read
forum_collection = conn["forum"]
user_collection = conn["user"]

# crrétion du pointeur
cursor = forum_collection.find(filter=None, projection={'annotated_content_info': 0, '_id': 1})#.limit(5000)
nbre_docs = cursor.count()
print('nbre de doc: ', nbre_docs)


"""###Les N MOOC les plus populaires (nb users)"""
def n_Mooc_plus_populaires(nb_mooc=10):
    # Calculate the number of users for each course:course_id
    pipeline = [
        {
            "$group": {
                "_id": "$content.course_id",
                "users": { "$addToSet": "$content.username" }
            }
        },
        {
            "$project": {
                "course_id": "$_id",
                "user_count": { "$size": "$users" },
                "_id": 0
            }
        }
    ]

    results = forum_collection.aggregate(pipeline)

    df_mooc_users_num = pd.DataFrame(results).sort_values(by='user_count', ascending=False).head(nb_mooc)
    return df_mooc_users_num
df_mooc_populaires = n_Mooc_plus_populaires(nb_mooc=20)
print(df_mooc_populaires)



"""###Horizontale barplot"""

def bar_plot_asc(df_inpput,val_x,val_y,hover_name,color, titre='Titre du graphique'):
  #io.renderers.default='colab'
  df = df_inpput
  fig = px.bar(df_inpput, x=val_x, y=val_y, hover_name=hover_name , color=color)
  fig.update_layout( yaxis={'categoryorder': 'total ascending'})
  fig.update_layout(title_text=titre, title_x=0.5)
  res = fig
  return res

# def main():
#     # Les 10 cours qui ont le plus de user

#     df_mooc_populaires = n_Mooc_plus_populaires(nb_mooc=20)
#     print(df_mooc_populaires)

#     mooc_populaires_bar_plot = bar_plot_asc(df_mooc_populaires,"user_count","course_id","course_id","course_id", titre=f'Les {len(df_mooc_populaires)} Moocs les plus populaires')
#     mooc_populaires_bar_plot.show()

# if __name__ == '__main__':
#     main()

# # Les 10 cours qui ont le plus de user query sur mongodb
# pipeline = [
#     {
#         "$group": {
#             "_id": "$content.course_id",
#             "user_set": { "$addToSet": "$content.username" },
#             "user_count": { "$sum": 1 }
#         }
#     },
#     {
#         "$project": {
#             "_id": 1,
#             "user_count": { "$size": "$user_set" }
#         }
#     },
#     {
#         "$sort": {
#             "user_count": -1
#         }
#     },
#     {
#         "$limit": 10
#     }
# ]
# results = forum_collection.aggregate(pipeline)
# for cours in results:
#     print(cours["_id"])
#     print("User count:", cours["user_count"])


# Define the query
# query = {"username": {"$exists": True}}



# Execute the query
results = user_collection.find()#.limit(1)


# # Print the results
for document in results:
    keys = [k for k in document.keys() if k not in ['_id', 'id', 'username']]
    username = document["username"]
    # print(username)
    for course in keys:
        # print(course )
        sub_doc = document[course ]
        grade = sub_doc.get("grade")
        certificate_eligible = sub_doc.get("Certificate Eligible")
        gender = sub_doc.get("gender")
        print(username, course, grade, certificate_eligible, gender)
        
    


