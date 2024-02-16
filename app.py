import streamlit as st
import pickle
import pandas as pd
import requests

shows_v1 = pickle.load(open("pkl-files/shows_v1.pkl", "rb"))
shows_v1 = pd.DataFrame(shows_v1)
similarity_v1 = pickle.load(open("pkl-files/similarity_v1.pkl", "rb"))

shows_v2 = pickle.load(open("pkl-files/shows_v2.pkl", "rb"))
shows_v2 = pd.DataFrame(shows_v2)
similarity_v2 = pickle.load(open("pkl-files/similarity_v2.pkl", "rb"))

shows_v3 = pickle.load(open("pkl-files/shows_v3.pkl", "rb"))
shows_v3 = pd.DataFrame(shows_v3)
similarity_v3 = pickle.load(open("pkl-files/similarity_v3.pkl", "rb"))


def get_movie_poster(movie_title):
    api_key = "99f3b2c3"
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    poster_url = data.get("Poster", "")
    return poster_url


def recommend(movie_title, shows, similarity):
    movie_index = shows[shows["title"] == movie_title].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[
        1:6
    ]

    recommended_movies = []
    recommended_movies_posters = []
    for movie in movies_list:
        movie_name = shows.iloc[movie[0]].title
        recommended_movies.append(movie_name)
        poster_url = get_movie_poster(movie_name)
        if poster_url and poster_url != "N/A":
            recommended_movies_posters.append(poster_url)
        else:
            recommended_movies_posters.append("images/placeholder.jpg")
    return recommended_movies, recommended_movies_posters


st.set_page_config(
    page_title="Show Matcher: Find Your Next Binge-Worthy Series",
    page_icon="🔍",
    layout="wide",
)


st.title("📺 Explore Related Shows!")
selected_movie = st.selectbox(
    "Enter You Favorite Show Name",
    [""] + list(shows_v1["title"].values),
)

if st.button("Recommend"):
    with st.spinner("AI is finding the best recommendations for you..."):
        recommended_movies_v1, posters_v1 = recommend(selected_movie, shows_v1, similarity_v1)
        recommended_movies_v2, posters_v2 = recommend(selected_movie, shows_v2, similarity_v2)
        recommended_movies_v3, posters_v3 = recommend(selected_movie, shows_v3, similarity_v3)
    tab1,tab2,tab3 = st.tabs(['Most Related Shows', 'Alternate Related Shows', 'Additional Shows with Similar Themes'])
    with tab1:
        st.title("Most Related Shows")
        num_columns = 5
        cols = st.columns(num_columns, gap="medium")

        for i in range(min(len(recommended_movies_v1), num_columns)):
            with cols[i]:
                st.image(posters_v1[i])
                st.subheader(recommended_movies_v1[i])

    with tab2:
        st.title("Alternate Related Shows")
        num_columns = 5
        cols = st.columns(num_columns, gap="medium")

        for i in range(min(len(recommended_movies_v2), num_columns)):
            with cols[i]:
                st.image(posters_v2[i])
                st.subheader(recommended_movies_v2[i])

    with tab3:
            st.title("Additional Shows with Similar Themes")
            num_columns = 5
            cols = st.columns(num_columns, gap="medium")

            for i in range(min(len(recommended_movies_v3), num_columns)):
                with cols[i]:
                    st.image(posters_v3[i])
                    st.subheader(recommended_movies_v3[i])


# Most Related Shows
# Alternate Related Shows
# Additional Shows with Similar Themes


st.write(
    """
    <style>
    span.st-emotion-cache-10trblm.e1nzilvr1 {
    text-transform: capitalize;
}

.st-emotion-cache-fjmja9 {
    gap: 0.5rem;
}

.st-emotion-cache-434r0z.e1f1d6gn5 .st-emotion-cache-1v0mbdj.e115fcil1 {
    width: 100%;
    height: 370px;
}

.st-emotion-cache-434r0z.e1f1d6gn5 .st-emotion-cache-1v0mbdj.e115fcil1 img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
    </style>
    """,
    unsafe_allow_html=True,
)
