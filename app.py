from flask import Flask , render_template ,request
from datetime import date

from graphviz import render
from fetch import movie , movie_collection
import json
import requests
app = Flask(__name__)
import pandas as pd 

df2 = pd.read_csv('./datasets/tmdb_5000_movies.csv')
df2 = df2.reset_index()
all_titles = [df2['title'][i] for i in range(len(df2['title']))]
indices = pd.Series(df2.index , index=df2['title'])

@app.route('/',methods=['GET','POST'])
def home():
    if request.method =="GET":
        year = date.today().year
        url = f'http://api.themoviedb.org/3/discover/movie?api_key=da396cb4a1c47c5b912fda20fd3a3336&primary_release_year={year}&sort_by=popularity.desc'
        top_year = movie_collection()
        top_year.results = []
        top_year.fetch(url)
        print(top_year.results)
        genres = json.loads(requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key=da396cb4a1c47c5b912fda20fd3a3336&language=en-US").text)

        top_genre_collection = []
        for genre in genres['genres']:
            # print(genre['id'])
            genre_id = f'https://api.themoviedb.org/3/discover/movie?api_key=da396cb4a1c47c5b912fda20fd3a3336&with_genres={genre["id"]}&sort_by=popularity.desc'
            top_genre = movie_collection()
            top_genre.results = []
            top_genre.fetch(genre_id)
            top_genre_id = [top_genre.results, genre["name"]]
            top_genre_collection.append(top_genre_id)

        return render_template('home.html', top_year = top_year.results , year= year ,top_genre = top_genre_collection )

    else:
        key_word = request.form['query']
        # return key_word
        url = f"http://api.themoviedb.org/3/search/movie?api_key=da396cb4a1c47c5b912fda20fd3a3336&query={key_word}"
        movie_dic = movie_collection()
        movie_dic.results = []
        movie_dic.fetch(url)
        # print(movie_dic.results)

        return render_template("landing.html", movie=movie_dic.results , key_word=key_word )



@app.route('/details/<ids>',methods=['GET','POST'])
def details(ids):
    if request.method == 'GET':
        url = f"http://api.themoviedb.org/3/movie/{ids}?api_key=da396cb4a1c47c5b912fda20fd3a3336"
        data = json.loads(requests.get(url).text)
        data_json = movie(data["id"],data["title"],data["poster_path"],data["vote_average"],data["release_date"],data["overview"])
        print(data_json)
        
        return render_template('details.html' , movie = data_json)

from ml import RECOMMAND
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
@app.route('/recommend', methods=['GET' , 'POST'])
def recommend():
    if request.method == 'GET':
        return render_template('recommend.html')

    elif request.method == 'POST':
        
        print(len(all_titles))
        m_name = request.form['movie_name']
        # print(m_name.title())
        m_name = m_name.title()
        if m_name not in all_titles:
            return render_template('nagative.html', name= m_name)
        else:
            recommander = RECOMMAND(TfidfVectorizer)
            result_final = recommander.get_recommandation(m_name)
            print(result_final)
            data = []
            for i in range(len(result_final)):
                data.append((result_final.iloc[i][0], result_final.iloc[i][1]))
            print(data)

            return render_template('positive.html', movie_data=data , search_name=m_name)
            # return render_template('positive.html' , movie_data=data, search_name=m_name)
if __name__ == "__main__":
    app.run(debug=True)