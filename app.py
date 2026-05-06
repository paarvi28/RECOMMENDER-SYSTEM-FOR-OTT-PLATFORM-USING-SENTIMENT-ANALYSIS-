import streamlit as st
import pandas as pd
import requests

# ------------------ CONFIG ------------------ #
st.set_page_config(layout="wide")

TMDB_API_KEY = "11da9eae256550559571dda4eb783d7c"  

# ------------------ STYLE ------------------ #
st.markdown("""
<style>
.main { background-color: #0e1117; }
h1, h2, h3 { color: white; }
</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------ #
st.title("🎬 BingeWatch")
st.markdown("AI-powered OTT Recommendation System")

# ------------------ LOAD DATA ------------------ #
df = pd.read_csv("final_movies.csv", encoding="latin1")
df.columns = df.columns.str.lower()

title_col = next((c for c in df.columns if 'title' in c), df.columns[0])
genre_col = next((c for c in df.columns if 'listed' in c), None)
desc_col = next((c for c in df.columns if 'description' in c or 'overview' in c), None)

# ------------------ TMDB FUNCTIONS ------------------ #
def get_movie_data(title):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
        res = requests.get(url).json()

        if res["results"]:
            movie = res["results"][0]
            poster = movie.get("poster_path")
            movie_id = movie.get("id")

            poster_url = f"https://image.tmdb.org/t/p/w500{poster}" if poster else None

            # trailer
            trailer_url = None
            if movie_id:
                vid_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}"
                vids = requests.get(vid_url).json()

                for v in vids.get("results", []):
                    if v["type"] == "Trailer":
                        trailer_url = f"https://www.youtube.com/watch?v={v['key']}"
                        break

            return poster_url, trailer_url

    except:
        return None, None

    return None, None

# ------------------ SENTIMENT ------------------ #
def get_sentiment(text):
    text = str(text).lower()
    pos = ['good','great','amazing','love','excellent']
    neg = ['bad','boring','worst','hate']

    score = sum(w in text for w in pos) - sum(w in text for w in neg)

    if score > 0: return "🟢 Positive"
    elif score < 0: return "🔴 Negative"
    else: return "⚪ Neutral"

if desc_col:
    df["sentiment"] = df[desc_col].apply(get_sentiment)
else:
    df["sentiment"] = "⚪ Neutral"

# ------------------ SEARCH ------------------ #
search = st.text_input("🔍 Search movies")

if genre_col:
    genre = st.selectbox("Genre", df[genre_col].dropna().unique())
else:
    genre = None

filtered_df = df.copy()

if genre:
    filtered_df = filtered_df[
        filtered_df[genre_col].astype(str).str.contains(genre, na=False)
    ]

if search:
    filtered_df = filtered_df[
        filtered_df[title_col].str.contains(search, case=False, na=False)
    ]

filtered_df = filtered_df.head(12)

# ------------------ UI ------------------ #
st.markdown("## 🔥 Recommended For You")

cols = st.columns(4)

for i, (_, row) in enumerate(filtered_df.iterrows()):
    col = cols[i % 4]

    with col:
        title = row[title_col]
        sentiment = row["sentiment"]

        poster, trailer = get_movie_data(title)

        if poster:
            st.image(poster)
        else:
            st.image("https://via.placeholder.com/300x400")

        st.markdown(f"**{title}**")
        st.write(sentiment)

        if trailer:
            st.markdown(f"[▶ Watch Trailer]({trailer})")
