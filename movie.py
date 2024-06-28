import pandas as pd
import streamlit as st
import pickle
import requests

st.title('Movie Recommendation System')
st.header('Content based Recommendations')sudi
model = pickle.load(open('movie_details.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
popular_movies = pickle.load(open('popular_movies.pkl', 'rb'))
df = pd.DataFrame(model)
popular_df = pd.DataFrame(popular_movies)


def fetch_poster(movie_id):

    url = "https://api.themoviedb.org/3/movie/{}?api_key=3bcb8b5e380adb5f6ee1088cf5577a89&language=en-US".format(
        movie_id)
    response = requests.get(url)
    dict = response.json()
    poster_path = dict['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie_name):
    index_position = df.index[df['title'] == movie_name][0]
    recommended_movies = []
    recommended_movies_posters = []
    for i in range(5):
        a = (sorted(list(enumerate(similarity[index_position])), key=lambda x: x[1], reverse=True)[1:6][i][0])
        movie_id = df.iloc[a]['movie_id']
        recommended_movies.append(df.iloc[a]['title'])
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


selected_movie = st.selectbox('Select a movie', df['title'].tolist())
if st.button('Recommend'):
    recommendations, recommended_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommendations[0])
        st.image(recommended_posters[0])
    with col2:
        st.text(recommendations[1])
        st.image(recommended_posters[1])

    with col3:
        st.text(recommendations[2])
        st.image(recommended_posters[2])
    with col4:
        st.text(recommendations[3])
        st.image(recommended_posters[3])
    with col5:
        st.text(recommendations[4])
        st.image(recommended_posters[4])

st.header('Popularity based Recommendations')


def popular_recommendations(genre1, genre2):
    l = []
    for i in range(popular_df.shape[0]):
        if (genre1 in popular_df.iloc[i]['genres']) and (genre2 in popular_df.iloc[i]['genres']):
            l.append(popular_df.iloc[i])
    users_df = pd.DataFrame(l)
    p = users_df.sort_values('popularity', ascending=False).iloc[0:10]['title'].values
    return p

x = []
for i in popular_movies['genres']:
    for j in i:
        x.append(j)
diff_genre = set(x)
genre1 = st.selectbox('Select a genre', diff_genre)
genre2 = st.selectbox('Select another genre', diff_genre)

if st.button('Recommend according to genre'):
    popular_movies_wrt_genre = popular_recommendations(genre1, genre2)
    for k in popular_movies_wrt_genre:
        st.write(k)
