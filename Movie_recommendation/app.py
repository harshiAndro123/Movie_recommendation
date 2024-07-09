import pickle
import streamlit as st
import requests

# Function to fetch movie poster
def fetch_poster(id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(id)
    data = requests.get(url)
    data=data.json()
    poster_path = data.get('poster_path')
    full_path = f"https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path

# Load movie data and similarity matrix
movie = pickle.load(open("movie_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movie_list = movie['title'].values

# Streamlit app header
st.header("Movie Recommender System")

# Movie selection box
selected_movie = st.selectbox("Select a movie:", movie_list)

# Recommendation function
def recommend(selected_movie):
    index = movie[movie['title'] == selected_movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[1:6]:
        # Fetch the movie id from the DataFrame
        id = movie.iloc[i[0]]['id']
        recommend_movie.append(movie.iloc[i[0]]['title'])
        recommend_poster.append(fetch_poster(id))
    return recommend_movie, recommend_poster

# Display recommendations on button click
if st.button('Recommend'):
    movie_name, movie_poster = recommend(selected_movie)
    col1, col2, col3, col4, col5= st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])