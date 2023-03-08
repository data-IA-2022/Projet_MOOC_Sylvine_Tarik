# I. Setup
#import
from sqlalchemy import text, create_engine
import pandas as pd
import numpy as np

# Preprocessing
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, RobustScaler, LabelEncoder
from sklearn.pipeline import Pipeline

from textblob import TextBlob, Blobber
from textblob_fr import PatternTagger, PatternAnalyzer

# modèle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import pickle


# import du dataset
# requetes sql qui vont bien pour faire un beau dataset, ou récup d'un pickle après traitement dans un autre fichier
# attention il faudra trier les données et retirer les anonymes, les admins

#dummy dataset pour entrainement
data = pd.read_csv("../../dummy_dataset.csv", sep = ",")
data["corpus"] = data["corpus"].fillna("") # remplacer les NA par des "" pour le concat body


# II. Prétraitement des données
# ajout des colonnes pour textblob: calcul polarity et subjectivity
tb = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())

polarity = []
subjectivity = []

for (i, row) in data.iterrows():
    # if i>10: quit()
    blob = tb(row['corpus'])
    # print(f"user: {row['user']} course :{row['course_id']} sentiment:{blob.sentiment}")
    polarity.append(blob.sentiment[0])
    subjectivity.append(blob.sentiment[1])


#update le dataset avec les nouvelles valeurs
data['polarity']=polarity
data['subjectivity']=subjectivity
# possibilité d'améliorer ce traitement mais tant pis pour le moment, priorité à un modèle qui tourne:
# détecter la langue, "lisser" les phrases = enlever la ponctuation, corriger les fautes, enlever les stop words...


# encoding de la target certificate_eligible (nécessaire si jamais logistic regression)
data['certificate_eligible'] = LabelEncoder().fit_transform(data['certificate_eligible'])
# à exporter en sérialisé pour récup les data


# III. Modele 

# fonction pour créer la pipeline
def create_pipe(model):
    # Categorical variables
    column_cat = ['gender', 'country', 'level_of_education']
    transfo_cat = Pipeline(steps=[
        ('imputation', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    # Numerical variables
    column_num = ['nb_threads', 'nb_comments', 'delai_1er_post', 'polarity', 'subjectivity']
    transfo_num = Pipeline(steps=[
        ('imputation', SimpleImputer(strategy='median')),
        ('scaling', RobustScaler())
    ])

    # Class ColumnTransformer : apply alls steps on the whole dataset
    preparation = ColumnTransformer(
        transformers=[
            ('data_cat', transfo_cat , column_cat),
            ('data_num', transfo_num , column_num)
         ])

    # Creation of the pipeline
    pipe = Pipeline(steps=[('preparation', preparation),
                            ('model',model)])

    return pipe


'''
#ICI JE CHERCHE JUSTE A APPLIQUER LA PIPELINE SUR LE DATASET SANS FAIRE DE GRIDSEARCH, ON GARDERA PAS FORCEMENT

# appliquer la pipeline sur le bon dataset
def pipe_res(target, model):
    X = data.drop(['user', 'course_id', 'corpus','grade','certificate_eligible'], axis=1)
    y = data[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    pipe = create_pipe(model)
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    print(f"Target = {target}, model = {model}, r2score= {r2_score(y_test, y_pred)}") 



print("-------------CLASSIFICATION : target = certificate_eligible-------------")
pipe_res("certificate_eligible", LogisticRegression())
pipe_res("certificate_eligible", SVC())
pipe_res("certificate_eligible", RandomForestClassifier())


print("-------------REGRESSION : target = grade-------------")
pipe_res("grade", LinearRegression())
pipe_res("grade", RandomForestRegressor())

quit()
'''


# Déclaration du grid search 
def grid_search_fun(target, model, parameters):
    X = data.drop(['user', 'course_id', 'corpus','grade','certificate_eligible'], axis=1)
    y = data[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    pipe = create_pipe(model)
    grid = GridSearchCV(pipe, parameters, scoring='r2', cv = 3, n_jobs =-1, verbose = 1)
    # fit le model
    grid.fit(X_train, y_train)

    # Evaluate cross validation performance 
    print("-----------------------------------------------------------------------")
    print(f"Target = {target}, model = {model}") 
    print("CV best params:", grid.best_params_)
    print("CV best score - R2:", grid.best_score_)

    # Make predictions
    y_pred = grid.predict(X_test)

    # Evaluate model performance
    print("Test score - R2:", r2_score(y_test, y_pred))
    return grid

# test du gridsearch sur le svc
params = {'model__kernel': ['linear', 'poly', 'rbf', 'sigmoid'] }  
modele = grid_search_fun("certificate_eligible", SVC(), params)


filename = 'finalized_model.sav'
pickle.dump(modele.best_estimator_, open(filename, 'wb'))
print("modele enregistré")

# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))
print("modèle chargé")

X = data.drop(['user', 'course_id', 'corpus','grade','certificate_eligible'], axis=1)
y = data['certificate_eligible']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

result = loaded_model.score(X_test, y_test)
print(result)


'''anticipation sur la prédiction par la suite:
on voudra entrer des données concernant l'utilisateur via un formulaire
nb: certaines de ces données devront être process hors du pipeline, notamment pour l'analyse de sentiments 
(car besoin de créer deux colonnes ). Il faudra penser à préprocess le corpus (si null, ""; sinon faire le preproc) 
et la target si on choisit la classif
'''



# soit cette liste l'ensemble des données entrées par l'utilisateur dans le formulaire
gender = "m"
country = "fr"
level_of_education = "hs"
nb_threads = 1
nb_comments = 2
# corpus = "c'est un roc, c'est un pic, c'est un cap, que dis-je c'est un cap, c'est une péninsule!"
corpus = "c'est nul, je n'aime pas, je suis subjectif et négatif"
delai_1er_post = 6

x_pred = [gender, country, level_of_education, nb_threads, nb_comments, corpus, delai_1er_post]
print(f"x pred avant = {x_pred}")
# process les data d'entrée
# traiter la façon dont on récupère les data vides: est-ce des Na? des ""? 
# je laisse la suite qui ici ne fait rien mais à adapter en fonction du résutalt du formulaire

# if corpus == "":
#     corpus = ""

tb = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
blob = tb(corpus)

polarity = (blob.sentiment[0])
subjectivity = (blob.sentiment[1])

x_pred.append(polarity)
x_pred.append(subjectivity)
print(f"x pred complet= {x_pred}")


# pred model
df_input = pd.DataFrame(np.array([x_pred]),
                    columns=["gender", "country", "level_of_education", "nb_threads", "nb_comments", "corpus", "delai_1er_post", "polarity", "subjectivity"])

y_pred = loaded_model.predict(df_input)

print(f"y pred = {y_pred}")
if y_pred == [1]:
    print("Cet utilisateur devrait valider le diplome")
else: 
    print("Cet utilisateur ne devrait pas valider le diplome")




