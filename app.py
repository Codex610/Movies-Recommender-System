import pickle
import streamlit as st
import pandas as pd
import requests

# ========== Custom CSS ==========
st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 40px !important;
        font-weight: 700;
        color: #FF4B4B;
        margin-bottom: 25px;
    }
    .recommend-card {
        padding: 10px;
        border-radius: 15px;
        background-color: #f9f9f9;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        text-align: center;
    }
    .movie-title {
        font-size: 16px;
        font-weight: 600;
        margin-top: 10px;
        color: #333;
    }
    img {
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# ========== Fetch poster ==========
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=87de717f13b0310ebf4f85b59fe9b337&language=en-US"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    except:
        return "https://via.placeholder.com/500x750?text=Poster+Unavailable"

# ========== Recommend function ==========
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# ========== Streamlit UI ==========
st.markdown('<h1 class="title">🎬 Movie Recommender System</h1>', unsafe_allow_html=True)

# Load data
movies = pickle.load(open('movies.pkl','rb'))
if not isinstance(movies, pd.DataFrame):
    movies = pd.DataFrame(movies)

similarity = pickle.load(open('similarity.pkl','rb'))

# Dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox("🔎 Search or select a movie:", movie_list)

# Show Recommendations
if st.button('✨ Show Recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)

    for idx, col in enumerate(cols):
        with col:
            st.markdown(
                f"""
                <div class="recommend-card">
                    <img src="{recommended_movie_posters[idx]}" width="150">
                    <div class="movie-title">{recommended_movie_names[idx]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
