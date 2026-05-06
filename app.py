import streamlit as st
import pandas as pd
import requests

# ---------------- CONFIG ---------------- #
st.set_page_config(layout="wide")

TMDB_API_KEY = "11da9eae256550559571dda4eb783d7c"

# ---------------- STYLE ---------------- #
st.markdown("""
<style>

/* FONT */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
    background-color: #0b0f1a;
}

/* HEADINGS */
h1 { font-size: 42px; color: white; }
h3 { font-size: 20px; color: #d1d5db; }

/* CARD */
.card {
    background: #111827;
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 20px;
    transition: 0.3s ease;
}
.card:hover {
    transform: scale(1.04);
}

/* TEXT */
.card-title {
    font-size: 16px;
    font-weight: 600;
    color: #f9fafb;
}

.positive { color: #22c55e; }
.negative { color: #ef4444; }
.neutral { color: #9ca3af; }

</style>
""", unsafe_allow_html=True)

/* CARD */
.card {
    background: #111827;
    border-radius: 12px;
    padding: 12px;
    margin-bottom: 20px;
    transition: 0.3s ease;
}
.card:hover {
    transform: scale(1.05);
}

/* CARD TITLE */
.card-title {
    font-size: 16px;
    font-weight: 600;
    color: #f9fafb;
}

/* SENTIMENT COLORS */
.positive { color: #22c55e; }
.negative { color: #ef4444; }
.neutral { color: #9ca3af; }

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ---------------- #
st.markdown("""
<h1>🎬 BingeWatch -- MoodWatch</h1>
<h3>Your AI-powered OTT Recommendation Engine</h3>
""", unsafe_allow_html=True)

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

    if score > 0:
        return "🟢 Positive"
    elif score < 0:
        return "🔴 Negative"
    else:
        return "⚪ Neutral"

if desc_col:
    df["sentiment"] = df[desc_col].apply(get_sentiment)
else:
    df["sentiment"] = "⚪ Neutral"

# ---------------- TMDB FUNCTION ---------------- #
@st.cache_data(show_spinner=False)
def get_movie_data(title):
    try:
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
        res = requests.get(search_url).json()

        if res.get("results"):
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
                    if v.get("type") == "Trailer":
                        trailer_url = f"https://www.youtube.com/watch?v={v['key']}"
                        break

            return poster_url, trailer_url

    except:
        return None, None

    return None, None

# ---------------- SEARCH + FILTER ---------------- #
st.markdown("## 🔍 Discover")

col1, col2 = st.columns([2, 1])

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
        filtered_df[title_col].astype(str).str.contains(search, case=False, na=False)
    ]

filtered_df = filtered_df.head(12)

# ---------------- TRENDING ---------------- #
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

        if "Positive" in sentiment:
            sentiment_class = "positive"
        elif "Negative" in sentiment:
            sentiment_class = "negative"
        else:
            sentiment_class = "neutral"

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.image(poster if poster else "https://via.placeholder.com/300x400")

        st.markdown(f'<div class="card-title">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{sentiment_class}">{sentiment}</div>', unsafe_allow_html=True)

        if trailer:
            with st.expander("▶ Watch Trailer"):
                st.video(trailer)

        st.markdown('</div>', unsafe_allow_html=True)
