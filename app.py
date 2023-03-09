from flask import Flask, render_template, request
from analyse import bar_plot_asc, n_Mooc_plus_populaires, dataset
import plotly.graph_objs as go
# For ploting graph / Visualization
import plotly.express as px
from plotly.io import to_json
from flask_bootstrap import Bootstrap
import pandas as pd
import numpy as np
import pickle
from unidecode import unidecode
from markupsafe import escape
import numpy as np
from textblob import TextBlob, Blobber
from textblob_fr import PatternTagger, PatternAnalyzer



import os.path

model = os.path.join("data", "my_best_pipeline.pkl")
filename = os.path.join("data",'modele_redump.sav')
app = Flask(__name__)
bootstrap = Bootstrap(app)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/analyse')
def analyse():
    selected_mooc = 10
    df_mooc_populaires = n_Mooc_plus_populaires(nb_mooc=selected_mooc)
    # print(df_mooc_populaires)
    mooc_populaires_bar_plot = bar_plot_asc(df_mooc_populaires,"user_count","course_id","course_id","course_id", titre=f'Les {len(df_mooc_populaires)} Moocs les plus populaires')
    mooc_populaires_bar_plot
    # Generate HTML code for Plotly px figure
    plot_html = mooc_populaires_bar_plot.to_html(full_html=False)
    return render_template('analyse.html', plot=plot_html)

 
   

@app.route('/model', methods=['GET', 'POST'])
def model():
    df=pd.read_csv(dataset)
    print(request.method)
    pays_dict = {'--': np.nan, 'France': 'FR', 'Mauritanie': 'MR',
                 'Maroc': 'MA', 'Togo': 'TG', 'Cameroun': 'CM', 'Algérie': 'DZ',
                  'Côte d\'Ivoire': 'CI', 'Belgique': 'BE', 'Tunisie': 'TN',
                   'Madagascar': 'MG', 'Indonésie': 'ID', 'Russie': 'RU',
                    'République démocratique du Congo': 'CD', 'Suisse': 'CH',
                    'Canada': 'CA', 'Chine continentale': 'CN', 'Bénin': 'BJ',
                    'Colombie': 'CO', 'Comores': 'KM', 'Polynésie française': 'PF',
                    'Réunion': 'RE', 'Singapour': 'SG', 'Guadeloupe': 'GP', 'Thaïlande': 'TH',
                    'Sénégal': 'SN', 'Martinique': 'MQ', 'Gabon': 'GA', 'Guyane française': 'GF',
                    'Mali': 'ML', 'Andorre': 'AD', 'Costa Rica': 'CR', 'Irlande': 'IE',
                    'Luxembourg': 'LU', 'Émirats arabes unis': 'AE', 'Australie': 'AU',
                    'République centrafricaine': 'CF', 'Royaume-Uni': 'GB'}
    pays = pays_dict.keys()
    level_educ_dict= {'--': np.nan,
    "Doctorat" : "p",
    "Master ou diplôme professionnel" : "m", 
    "Diplôme de premier cycle supérieur" : "b", 
    "Niveau associé": "a", 
    "Lycéé / enseignement secondaire" : "hs", 
    "Collège / enseignement secondaire inférieur" : "jhs", 
    "Enseignement primaire" : "el", 
    "Pas de Formation Scolaire" : "none", 
    "Autres Etudes" : "other"}
    level_educ = level_educ_dict.keys()

    if request.method == 'POST':
        print(request.form)
        user = request.form.get('user', np.nan)
        gender = request.form.get('gender', np.nan)
        country = request.form.get('country', np.nan)
        level_of_education = request.form.get('level_of_education', np.nan)
        nb_threads = request.form.get('nb_threads', np.nan)
        nb_comments = request.form.get('nb_comments', np.nan)
        corpus = request.form.get('concat_bodys', '')
        delai_1er_post = request.form.get('delai_1er_post', np.nan)
        # Use values to run prediction model and get results
        # prétraitement du corpus
        #lower case
        corpus = corpus.lower()
        # envlever les accents
        corpus= unidecode(corpus)
        # analyse de sentiments
        tb = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
        blob = tb(corpus)

        polarity = (blob.sentiment[0])
        subjectivity = (blob.sentiment[1])
        # définition du df pour la prédiction
        input = [gender, country, level_of_education, nb_threads, nb_comments, corpus, delai_1er_post, polarity, subjectivity]
        for i in range(len(input)):
            if input[i] == 'nan':
                input[i] = np.NaN

        df_input = pd.DataFrame(np.array([input]),
                            columns=["gender", "country", "level_of_education", "nb_threads", "nb_comments", "corpus", "delai_1er_post", "polarity", "subjectivity"])
        print(df_input)
        # import model avec pycaret
        # loaded_model = model
        # import model avec pycaret
        loaded_model = pickle.load(open(filename, 'rb'))
        # prediction avec le modele
        y_pred = loaded_model.predict(df_input)

        # print(f"y pred = {y_pred}")

        if y_pred == [1]:
            result = f"L'utilisateur {user} devrait valider le diplome"
        else: 
            result = f"L'utilisateur {user} ne devrait pas valider le diplome"
        return render_template('model.html', prediction=result, pays=pays, level_educ=level_educ)
    else:
        return render_template('model.html', pays=pays, level_educ=level_educ)

if __name__ == '__main__':
    app.run(debug=True)