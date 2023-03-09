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


import numpy as np

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
    pays_dict = {'--': np.nan, 'République française': 'FR', 'Mauritanie': 'MR',
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
        user = request.form['user']
        gender = request.form['gender']
        country = request.form['country']
        level_of_education = request.form['level_of_education']
        course_id = request.form['course_id']
        nb_threads = request.form['nb_threads']
        nb_comments = request.form['nb_comments']
        concat_bodys = request.form['concat_bodys']
        delai_1er_post = request.form['delai_1er_post']
        grade = request.form['grade']
        certificate_eligible = request.form['certificate_eligible']
        # Use values to run prediction model and get results
        # ...
        return render_template('model.html', prediction=result, pays=pays, level_educ=level_educ)
    else:
        return render_template('model.html', pays=pays, level_educ=level_educ)

if __name__ == '__main__':
    app.run(debug=True)