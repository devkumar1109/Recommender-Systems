import pandas as pd
import streamlit as st
import pickle
import numpy as np

st.title('Books Recommendation System')

popular_books_dict = pickle.load(open('popular_books_dict.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))
books_ratings_dict = pickle.load(open('books_ratings_dict.pkl', 'rb'))


popular_books = pd.DataFrame(popular_books_dict)
books_ratings = pd.DataFrame(books_ratings_dict)


def recommend(book_title):
    book_name = list(pt.index)
    idx = book_name.index(book_title)
    book_recommendation = []
    book_author = []
    book_image_url = []
    for i in range(5):
        a = sorted(list(enumerate(similarity_scores[idx])), key=lambda x: x[1], reverse=True)[1:6][i][0]
        book_recommendation.append(pt.index[a])
        book_author.append(books_ratings[books_ratings['Book-Title'] == pt.index[a]]['Book-Author'].unique()[0])
        book_image_url.append(books_ratings[books_ratings['Book-Title'] == pt.index[a]]['Image-URL-M'].unique()[0])
    return book_recommendation, book_author, book_image_url


selected_book = st.selectbox('Select a book', pt.index)
if st.button('Recommend'):
    recommendations, authors, image = recommend(selected_book)
    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]
    for i in range(0,5):
        with cols[i]:
            st.markdown(f"<img src='{image[i]}' style='border: 5px solid black; width: 100%;'/>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:19px; font-weight:bold;'>By {recommendations[i]}</p>", unsafe_allow_html=True)
            st.write('By: ', authors[i])






