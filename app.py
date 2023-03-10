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
import db_connection as db_con
from pycaret.classification import load_model, predict_model
from EDA_notebook import fig_gender, fig_users_genre, fig_user_pays,fig_user_level, fig_user_mooc_success, fig_user_message, fig_success_nb_messages

import os.path
classification_model = os.path.join("data", "my_best_pipeline")
model = load_model(classification_model)

filename = os.path.join("data",'modele_redump.sav')

# # Connexion à mysql
# conn_mysql_datalab = db_con.connect_to_db(config_file='config.yaml', section='mysql_local_mooc', ssh=False, local_port=None, ssh_section= 'ssh_tunnel_datalab')
# variable = '21GG21'
# course_var = 'MinesTelecom/04017S02/session02'
# query = "SELECT corpus FROM dataset WHERE user = '21GG21' AND course_id = 'MinesTelecom/04017S02/session02'"
# # encode the query parameters as bytes
# variable_bytes = variable.encode('utf-8')
# course_var_bytes = course_var.encode('utf-8')
# message_query_user = conn_mysql_datalab.execute(query, variable_bytes,course_var_bytes) 
# results = message_query_user.fetchall()
# print(results)
# conn_mysql_datalab.close()

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

    #subplot gender
    fig_gender
    subplot_gender_html = fig_gender.to_html(full_html=False)
    #user genre
    fig_users_genre
    plot_user_gender = fig_users_genre.to_html(full_html=False)
    #user per country
    fig_user_pays
    plot_user_pays = fig_user_pays.to_html(full_html=False)
    #plot users level of educ
    fig_user_level
    plot_user_level = fig_user_level.to_html(full_html=False)
    # bar plot user par ooc avec taux de réussite
    fig_user_mooc_success
    barplot_user_mooc_success = fig_user_mooc_success.to_html(full_html=False)
    # bar chart nb message par user
    fig_user_message
    barplot_message_user = fig_user_message.to_html(full_html=False)
    # scatter plot success nb message
    fig_success_nb_messages
    scatter_messages_success = fig_success_nb_messages.to_html(full_html=False)





    return render_template('analyse.html', plot=plot_html, subplot=subplot_gender_html,piechart_user_gender=plot_user_gender,piechart_user_pays = plot_user_pays, piechart_user_lvl = plot_user_level,
                            barchart_user_mooc_success = barplot_user_mooc_success,barchart_user_message = barplot_message_user, scatter_mess_success = scatter_messages_success)

 
   

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
        country = pays_dict.get(request.form.get('country', np.nan))
        level_of_education = level_educ_dict.get(request.form.get('level_of_education', np.nan))
        nb_threads_str = request.form.get('nb_threads', np.nan)
        if nb_threads_str:
            nb_threads = int(nb_threads_str)
        else:
            nb_threads = np.nan
        nb_comments_str = request.form.get('nb_comments', np.nan)
        if nb_comments_str:
            nb_comments = int(nb_comments_str)
        else:
            nb_comments = np.nan
        corpus = request.form.get('concat_bodys', '')
        delai_1er_post_str = request.form.get('delai_1er_post', np.nan)
        if delai_1er_post_str:
            delai_1er_post = int(delai_1er_post_str)
        else:
            delai_1er_post = np.nan
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
        df_input = pd.DataFrame(columns=["gender", "country", "level_of_education", "nb_threads", "nb_comments", "delai_1er_post", "polarity", "subjectivity"])
        df_input.loc[0] = [gender, country, level_of_education, nb_threads, nb_comments, delai_1er_post, polarity, subjectivity ]
        # import model avec pycaret
        # loaded_model = model
        # import model avec pycaret
        loaded_model = pickle.load(open(filename, 'rb'))
        # prediction avec le modele
        y_pred = loaded_model.predict(df_input)
        # y_pred = predict_model(model, data=df_input)
        # print(f"y pred = {y_pred}") 
        if y_pred == [1]:
            result = f"L'utilisateur {user} devrait valider le diplome"
        else: 
            result = f"L'utilisateur {user} ne devrait pas valider le diplome"
        return render_template('model.html', prediction=result, pays=pays, level_educ=level_educ,table = df_input.to_html())
    else:
        return render_template('model.html', pays=pays, level_educ=level_educ)

if __name__ == '__main__':
    app.run(debug=True)