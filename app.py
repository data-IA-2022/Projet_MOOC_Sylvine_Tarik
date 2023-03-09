from flask import Flask, render_template, request
from analyse import bar_plot_asc, n_Mooc_plus_populaires, dataset
import plotly.graph_objs as go
# For ploting graph / Visualization
import plotly.express as px
from plotly.io import to_json
from flask_bootstrap import Bootstrap
import pandas as pd


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
    cours = df['course_id'].unique()
    pays = df['country'].unique()
    level_educ = df['level_of_education'].unique()
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
        return render_template('model.html', prediction=result, cours=cours, pays=pays, level_educ=level_educ)
    else:
        return render_template('model.html', cours=cours, pays=pays, level_educ=level_educ)

if __name__ == '__main__':
    app.run(debug=True)