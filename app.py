import streamlit as st
import pandas as pd
import requests

# ---------------- CONFIG ---------------- #
st.set_page_config(layout="wide")

TMDB_API_KEY = "11da9eae256550559571dda4eb783d7c" 

# ---------------- STYLE ---------------- #
st.markdown("""
<style>
body { background-color: #0e1117; }

.card {
    background-color:#111;
    border-radius:12px;
    overflow:hidden;
    transition:0.3s;
}
.card:hover {
    transform: scale(1.05);
}

.title {
    color:white;
    font-size:16px;
    font-weight:600;
}

.sentiment {
    font-size:13px;
}

.section-title {
    color:white;
    margin-top:20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ---------------- #
st.title("🎬 BingeWatch")
st.caption("Netflix-style AI Recommendation System")

# ---------------- LOAD DATA ---------------- #
df = pd.read_csv("final_movies.csv", encoding="latin1")
df.columns = df.columns.str.lower()

title_col = next((c for c in df.columns if 'title' in c), df.columns[0])
genre_col = next((c for c in df.columns if 'listed' in c), None)
desc_col = next((c for c in df.columns if 'description' in c or 'overview' in c), None)

# ---------------- SENTIMENT ---------------- #
def get_sentiment(text):
    text = str(text).lower()
    pos = ['good','great','amazing','love']
    neg = ['bad','boring','worst','hate']
    score = sum(w in text for w in pos) - sum(w in text for w in neg)

    if score > 0: return "🟢 Positive"
    elif score < 0: return "🔴 Negative"
    else: return "⚪ Neutral"

if desc_col:
    df["sentiment"] = df[desc_col].apply(get_sentiment)
else:
    df["sentiment"] = "⚪ Neutral"

# ---------------- TMDB ---------------- #
@st.cache_data(show_spinner=False)
def get_movie_data(title):
    try:
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
        res = requests.get(search_url).json()

        if res["results"]:
            movie = res["results"][0]
            poster = movie.get("poster_path")
            movie_id = movie.get("id")

            poster_url = f"https://image.tmdb.org/t/p/w500{poster}" if poster else None

            trailer_url = None
            if movie_id:
                vids = requests.get(
                    f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}"
                ).json()

                for v in vids.get("results", []):
                    if v["type"] == "Trailer":
                        trailer_url = f"https://www.youtube.com/watch?v={v['key']}"
                        break

            return poster_url, trailer_url
    except:
        return None, None

    return None, None

# ---------------- SEARCH + FILTER ---------------- #
st.markdown("## 🔍 Discover")

col1, col2 = st.columns([2,1])

with col1:
    search = st.text_input("Search movies")

with col2:
    genre = st.selectbox("Genre", df[genre_col].dropna().unique()) if genre_col else None

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

# ---------------- TRENDING ROW ---------------- #
st.markdown("## 🔥 Trending Now")

trend_cols = st.columns(6)

for i, (_, row) in enumerate(filtered_df.head(6).iterrows()):
    with trend_cols[i]:
        poster, _ = get_movie_data(row[title_col])
        st.image(poster if poster else "https://via.placeholder.com/200x300")

# ---------------- MAIN GRID ---------------- #
st.markdown("## 🎬 Recommended For You")

cols = st.columns(4)

for i, (_, row) in enumerate(filtered_df.iterrows()):
    col = cols[i % 4]

    with col:
        title = row[title_col]
        sentiment = row["sentiment"]

        poster, trailer = get_movie_data(title)

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.image(poster if poster else "https://via.placeholder.com/300x400")

        st.markdown(f'<div class="title">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sentiment">{sentiment}</div>', unsafe_allow_html=True)

        # 🎬 TRAILER BUTTON
        if trailer:
            with st.expander("▶ Watch Trailer"):
                st.video(trailer)

        st.markdown('</div>', unsafe_allow_html=True)
