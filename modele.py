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



# import du dataset
# requetes sql qui vont bien pour faire un beau dataset, ou récup d'un pickle après traitement dans un autre fichier
# attention il faudra trier les données et retirer les anonymes, les admins

#dummy dataset pour entrainement
data = pd.read_csv("../../dummy_dataset.csv", sep = ",")
data["concat_bodys"] = data["concat_bodys"].fillna("") # remplacer les NA par des "" pour le concat body


# II. Prétraitement des données
# ajout des colonnes pour textblob: calcul polarity et subjectivity
tb = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())

polarity = []
subjectivity = []

for (i, row) in data.iterrows():
    # if i>10: quit()
    blob = tb(row['concat_bodys'])
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
ICI JE CHERCHE JUSTE A APPLIQUER LA PIPELINE SUR LE DATASET SANS FAIRE DE GRIDSEARCH, ON GARDERA PAS FORCEMENT

# appliquer la pipeline sur le bon dataset
def pipe_res(target, model):
    X = data.drop(['user', 'course_id', 'concat_bodys','grade','certificate_eligible'], axis=1)
    y = data[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    pipe = create_pipe(model)
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    print(f"Target = {target}, model = {model}, r2score= {r2_score(y_test, y_pred)}") 



print("-------------CLASSIFICATION : target = certificate_eligible-------------")
## logistic regression 
pipe_res("certificate_eligible", LogisticRegression())
pipe_res("certificate_eligible", SVC())
pipe_res("certificate_eligible", RandomForestClassifier())


print("-------------REGRESSION : target = grade-------------")
pipe_res("grade", LinearRegression())
pipe_res("grade", RandomForestRegressor())
'''



# Déclaration du grid search 
def grid_search_fun(target, model, parameters):
    X = data.drop(['user', 'course_id', 'concat_bodys','grade','certificate_eligible'], axis=1)
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

# test du gridsearch sur le svc
params = {'model__kernel': ['linear', 'poly', 'rbf', 'sigmoid'] }  
grid_search_fun("certificate_eligible", SVC(), params)
quit()




'''anticipation sur la prédiction par la suite:
on voudra entrer des données concernant l'utilisateur via un formulaire
nb: certaines de ces données devront être process hors du pipeline, notamment pour l'analyse de sentiments 
(car besoin de créer deux colonnes ). Il faudra penser à préprocess le concat_bodys (si null, ""; sinon faire le preproc) 
et la target si on choisit la classif
'''