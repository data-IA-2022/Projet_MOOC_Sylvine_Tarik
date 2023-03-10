#!/usr/bin/env python
# coding: utf-8

# # I. Setup

# In[58]:


# import
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from sklearn.preprocessing import OneHotEncoder, RobustScaler, LabelEncoder

import seaborn as sns
import matplotlib.pyplot as plt
from unidecode import unidecode
from textblob import TextBlob, Blobber
from textblob_fr import PatternTagger, PatternAnalyzer


from utils import data_preproc
import os.path
data_csv = os.path.join("data", "dataset.csv")
#pour appli


# In[73]:


# import dataset et preproc
data = pd.read_csv(data_csv, sep = ",")

#pour appli

# # drop la colonne total_length
# data = data.drop("total_length", axis=1)

# # drop les lignes où certificate_eligible ou grade = na 
# data.dropna(subset=['certificate_eligible', 'grade'], inplace = True) 

# # binarise la variable certificate_eligible
# data['diplome'] = LabelEncoder().fit_transform(data['certificate_eligible'])

# data.head()


# In[3]:


# def data_preproc(data):
#     #garde seulement lignes où certificate_eligible et grade ne sont pas null
#     data.dropna(subset=['certificate_eligible', 'grade'], inplace = True)

#     # vire colonne inutile total_length
#     data = data.drop("total_length", axis=1)

#     # encode le label
#     data['certificate_eligible'] = LabelEncoder().fit_transform(data['certificate_eligible'])

#     #prépare le corpus pour textblob
#     data["corpus"]= data["corpus"].str.lower()
#     # enlever les accents
#     unidec_corpus = []
#     for (i, row) in data.iterrows():
#         truc = unidecode(row['corpus'])
#         # #print(f"user: {row['user']} course :{row['course_id']} new_corp:{truc[:25]}")
#         unidec_corpus.append(truc)

#     data["corpus"] = unidec_corpus

#     tb = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())

#     polarity = []
#     subjectivity = []

#     for (i, row) in data.iterrows():
#         # if i>10: quit()
#         blob = tb(row['corpus'])
#         # #print(f"user: {row['user']} course :{row['course_id']} sentiment:{blob.sentiment}")
#         polarity.append(blob.sentiment[0])
#         subjectivity.append(blob.sentiment[1])

#     #update le dataset avec les nouvelles valeurs
#     data['polarity']=polarity
#     data['subjectivity']=subjectivity

#     return(data)


# In[5]:


data = data_preproc(data)
#pour appli


# In[ ]:


data.head()


# In[5]:


data.describe(include = object)


# In[6]:


data.describe(exclude = object)


# In[69]:


data.course_id.unique()


# # II. Plots

# ## 1. Par user/mooc (n= 5349)

# In[7]:


data.shape


# In[8]:


sns.heatmap(data.corr())
#pour appli


# 

# plot certif_elig selon genre

# In[6]:


data_gender = data[data.certificate_eligible == 1].groupby('gender', dropna=False)['certificate_eligible'].count().reset_index()
data_gender0 = data[data.certificate_eligible == 0].groupby('gender', dropna=False)['certificate_eligible'].count().reset_index()

data_gender = data_gender.rename(columns={'certificate_eligible':'Yes'})
data_gender0 = data_gender0.rename(columns={'certificate_eligible':'No'})
data_gender['No'] = data_gender0['No']

#print(data_gender)
#pour appli


# In[23]:


fig_gender = make_subplots(rows=1, cols=3, specs=[[{"type": "pie"},{"type": "pie"},{"type": "pie"}]],
                    subplot_titles=("Femmes", "Hommes", "Non communiqué"))

#gender f
fig_gender.add_trace(go.Pie(
     values=data_gender.iloc[[0], [1,2]].values.tolist()[0],
     labels=["Yes","No"
             ],
#      domain={x: [0.5, 1], y: [0, .5]},
     name="f"), 
     row=1, col=1)

#gender m
fig_gender.add_trace(go.Pie(
     values=data_gender.iloc[[1], [1,2]].values.tolist()[0],
     labels=["Yes","No"
             ],
#      domain=dict(x=[0.5, 1.0]),
     name="m"),
     row=1, col=2)

#gender m
fig_gender.add_trace(go.Pie(
     values=data_gender.iloc[[2], [1,2]].values.tolist()[0],
     labels=["Yes","No"
             ],
#      domain=dict(x=[0.5, 1.0]),
     name="NaN"),
     row=1, col=3)

fig_gender

#pour appli


# plot certif_elig selon level of edu

# In[24]:


data_level_of_education = data[data.certificate_eligible == 1].groupby('level_of_education', dropna=False)['certificate_eligible'].count().reset_index()
data_level_of_education0 = data[data.certificate_eligible == 0].groupby('level_of_education', dropna=False)['certificate_eligible'].count().reset_index()

data_level_of_education = data_level_of_education.rename(columns={'certificate_eligible':'Yes'})
data_level_of_education0 = data_level_of_education0.rename(columns={'certificate_eligible':'No'})
data_level_of_education['No'] = data_level_of_education0['No']


# In[50]:


# nb_pies = data_level_of_education.shape[0]
# range(nb_pies)
# for i in range(nb_pies):
#     r =  i//5 +1
#     c = i%5 + 1
#     #print(f"i = {i}, r = {r}, c = {c}")
   


# In[65]:


# nb_pies = data_level_of_education.shape[0]
# nb_pies


# In[ ]:


# nb_pies = data_level_of_education.shape[0]

# fig = make_subplots(rows=2, cols=5, specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}, {"type": "pie"}, {"type": "pie"}, {"type": "pie"}, {"type": "pie"}, {"type": "pie"}, {"type": "pie"}, {"type": "pie"}]],
#                     subplot_titles=tuple(data_level_of_education.level_of_education.tolist()))


# fig.add_trace(go.Pie(
#      values=data_level_of_education.iloc[[0], [1,2]].values.tolist()[0],
#      labels=["Yes","No"
#              ],
# #      domain=dict(x=[0.5, 1.0]),
#      name=data_level_of_education.level_of_education.tolist()[0]),
#      row=1, col=1)

# fig.add_trace(go.Pie(
#      values=data_level_of_education.iloc[[1], [1,2]].values.tolist()[0],
#      labels=["Yes","No"
#              ],
# #      domain=dict(x=[0.5, 1.0]),
#      name=data_level_of_education.level_of_education.tolist()[0]),
#      row=1, col=2)

# fig.add_trace(go.Pie(
#      values=data_level_of_education.iloc[[2], [1,2]].values.tolist()[0],
#      labels=["Yes","No"
#              ],
# #      domain=dict(x=[0.5, 1.0]),
#      name=data_level_of_education.level_of_education.tolist()[0]),
#      row=1, col=3)

# fig.add_trace(go.Pie(
#      values=data_level_of_education.iloc[[3], [1,2]].values.tolist()[0],
#      labels=["Yes","No"
#              ],
# #      domain=dict(x=[0.5, 1.0]),
#      name=data_level_of_education.level_of_education.tolist()[0]),
#      row=1, col=4)

# fig.add_trace(go.Pie(
#      values=data_level_of_education.iloc[[4], [1,2]].values.tolist()[0],
#      labels=["Yes","No"
#              ],
# #      domain=dict(x=[0.5, 1.0]),
#      name=data_level_of_education.level_of_education.tolist()[0]),
#      row=1, col=5)

# fig.add_trace(go.Pie(
#      values=data_level_of_education.iloc[[5], [1,2]].values.tolist()[0],
#      labels=["Yes","No"
#              ],
# #      domain=dict(x=[0.5, 1.0]),
#      name=data_level_of_education.level_of_education.tolist()[0]),
#      row=2, col=1)

# fig.add_trace(go.Pie(
#      values=data_level_of_education.iloc[[6], [1,2]].values.tolist()[0],
#      labels=["Yes","No"
#              ],
# #      domain=dict(x=[0.5, 1.0]),
#      name=data_level_of_education.level_of_education.tolist()[0]),
#      row=2, col=2)

# fig.add_trace(go.Pie(
#      values=data_level_of_education.iloc[[7], [1,2]].values.tolist()[0],
#      labels=["Yes","No"
#              ],
# #      domain=dict(x=[0.5, 1.0]),
#      name=data_level_of_education.level_of_education.tolist()[0]),
#      row=2, col=3)

# fig.add_trace(go.Pie(
#      values=data_level_of_education.iloc[[8], [1,2]].values.tolist()[0],
#      labels=["Yes","No"
#              ],
# #      domain=dict(x=[0.5, 1.0]),
#      name=data_level_of_education.level_of_education.tolist()[0]),
#      row=2, col=4)

# fig.add_trace(go.Pie(
#      values=data_level_of_education.iloc[[9], [1,2]].values.tolist()[0],
#      labels=["Yes","No"
#              ],
# #      domain=dict(x=[0.5, 1.0]),
#      name=data_level_of_education.level_of_education.tolist()[0]),
#      row=2, col=5)


# fig



# ## Par user (n = 4329)

# In[10]:


# Création jeu de données avec une seule ligne par user
# count de mooc
data_by_user = data.groupby('user')['course_id'].count().reset_index()

# somme de threads et comments
nb_mess = data.groupby('user')[['nb_threads','nb_comments']].sum().reset_index()

#moyenne de delai de post du premier message
moy_delai = data.groupby('user')['delai_1er_post'].mean().reset_index()

# nb de diplomes
nb_diplome = data.groupby('user')['certificate_eligible'].sum().reset_index()

# rassembler les variables dans le df
data_by_user[['nb_threads','nb_comments']] = nb_mess[['nb_threads','nb_comments']]
data_by_user['moy_delai'] = moy_delai["delai_1er_post"]
data_by_user['nb_diplome'] = nb_diplome["certificate_eligible"]

#calcul de nouvelles variables intermediaires
data_by_user['nb_messages'] = data_by_user["nb_threads"] + data_by_user["nb_comments"]
data_by_user['prop_succes'] = data_by_user["nb_diplome"] / data_by_user["course_id"]
data_by_user = data_by_user.rename(columns = {"course_id" : "nb_mooc"})
# data_by_user

# on devrait pouvoir rajouter les infos de genre, country et level of ed avec une methode de groupby... peut etre unique?
gender = data.groupby('user')["gender"].first().reset_index()
data_by_user['gender'] = gender["gender"]

country = data.groupby('user')["country"].first().reset_index()
data_by_user['country'] = country["country"]

level_of_education = data.groupby('user')["level_of_education"].first().reset_index()
data_by_user['level_of_education'] = level_of_education["level_of_education"]

data_by_user

#pour appli


# ### Corr heatmap

# In[11]:


# correlation heatmap
sns.heatmap(data_by_user.corr())


# ### repartition des genres, country, level_of_ed

# In[12]:fig_users_genre


# pieplot du nb de genre
fig_users_genre = px.pie(data_by_user, 
             values='nb_mooc', 
             names='gender', 
             title='Répartition des genres des users')
fig_users_genre


# In[13]:


# pieplot du nb de country
fig_user_pays = px.pie(data_by_user, 
             values='nb_mooc', 
             names='country', 
             title='Répartition des pays des users')
fig_user_pays


# In[14]:


# pieplot du nb de levels_of_education
fig_user_level = px.pie(data_by_user, 
             values='nb_mooc', 
             names='level_of_education', 
             title="Répartition des niveaux d'étude des users")
fig_user_level
# se renseigner sur les significations !


# ### exploration des users pour repérer outliers

# In[15]:


# plot nb de mooc par user, mappé par le taux de succès
fig_user_mooc_success = px.bar(data_by_user.sort_values(by='nb_mooc', ascending = False)[:50], 
             x='user', 
             y='nb_mooc',
             title="Nombre de MOOC par user",
             color='prop_succes')
fig_user_mooc_success

#pour appli


# In[16]:


#  nb messages et threads par user
fig_user_message = px.bar(data_by_user.sort_values(by='nb_messages', ascending = False)[:50], 
             x="user", 
             y=["nb_threads", "nb_comments"], 
             title="Nb de messages par user")
fig_user_message
#pour appli


# In[17]:


# nb_threads par user
fig = px.bar(data_by_user.sort_values(by='nb_threads', ascending = False)[:100], 
             x="user", 
             y="nb_threads", 
             title="Nb de threads par user")
fig


# In[18]:


# prop succès en fonction du nb messages
fig_success_nb_messages = px.scatter(data_by_user, 
             x="nb_messages", 
             y="prop_succes",
             hover_name = "user",
             title="Prop succès selon nb messages")
fig_success_nb_messages


# In[19]:


fig = px.scatter(data_by_user, 
             x="nb_threads", 
             y="prop_succes", 
             hover_name = "user",
             title="Prop succès selon nb threads")
fig


# In[20]:


fig = px.scatter(data_by_user, 
             x="nb_comments", 
             y="prop_succes", 
             hover_name = "user",
             title="Prop succès selon nb comments")
fig


# Au vu de ces différentes infos, on va explorer le corpus pour les quelques points suspects

# In[71]:


#print(data[data.user == "EGo41"]["course_id"][:])


# In[70]:


pd.set_option('display.max_colwidth', None)
#print(data[data.user == "EGo41"]["corpus"][:])
pd.set_option('display.max_colwidth', 50)
# il répond aux questions: Emmanuel est bien un admin!!


# In[ ]:





# In[35]:


pd.set_option('display.max_colwidth', None)
#print(data[data.user == "trx337"]["corpus"][:])
pd.set_option('display.max_colwidth', 50)
# visiblement il pose des questions, ce n'est pas un admin


# In[37]:


pd.set_option('display.max_colwidth', None)
#print(data[data.user == "bgaultier"]["corpus"][:])
pd.set_option('display.max_colwidth', 50)
# c'est un admin !


# In[38]:


pd.set_option('display.max_colwidth', None)
#print(data[data.user == "EllaHamonic"]["corpus"][:])
pd.set_option('display.max_colwidth', 50)
# c'est un admin !


# In[40]:


pd.set_option('display.max_colwidth', None)
#print(data[data.user == "stiphaen"]["corpus"][:])
pd.set_option('display.max_colwidth', 50)
# c'est un admin !


# In[66]:


pd.set_option('display.max_colwidth', None)
#print(data[data.user == "JPBAUJOT"]["corpus"][:])
pd.set_option('display.max_colwidth', 50)
# ce n'est pas un admin


# In[67]:


pd.set_option('display.max_colwidth', None)
#print(data[data.user == "SteveToulouse"]["corpus"][:])
pd.set_option('display.max_colwidth', 50)
# ce n'est pas un admin

