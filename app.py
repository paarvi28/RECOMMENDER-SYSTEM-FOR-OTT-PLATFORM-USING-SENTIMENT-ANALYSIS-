import streamlit as st
import pandas as pd
import requests

# ---------------- CONFIG ---------------- #
st.set_page_config(layout="wide")

TMDB_API_KEY = "11da9eae256550559571dda4eb783d7c" 

# ---------------- STYLE ---------------- #
st.markdown("""
<style>

/* IMPORT FONT */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

/* GLOBAL */
html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
    background-color: #0b0f1a;
}

/* MAIN CONTAINER */
.main {
    background: linear-gradient(180deg, #0b0f1a 0%, #111827 100%);
}

/* HEADINGS */
h1 {
    font-size: 42px;
    font-weight: 700;
    color: #ffffff;
}

h2 {
    font-size: 28px;
    font-weight: 600;
    color: #e5e7eb;
}

h3 {
    font-size: 22px;
    font-weight: 500;
    color: #d1d5db;
}

/* TEXT */
p, span {
    font-size: 14px;
    color: #9ca3af;
}

/* INPUT BOX */
.stTextInput input {
    background-color: #1f2937;
    color: white;
    border-radius: 8px;
    border: 1px solid #374151;
}

/* SELECT BOX */
.stSelectbox div {
    background-color: #1f2937;
    color: white;
}

/* BUTTON */
.stButton button {
    background-color: #6366f1;
    color: white;
    border-radius: 8px;
    border: none;
}
.stButton button:hover {
    background-color: #4f46e5;
}

/* CARD DESIGN */
cols = st.columns(4)

for i, row in filtered_df.iterrows():
    col = cols[i % 4]

    with col:
        title = row.get(title_col, "No Title")
        rating = row.get(rating_col, "N/A") if rating_col else "N/A"
        description = str(row.get(desc_col, ""))[:90]
        sentiment = row.get('sentiment', "Neutral")

        # sentiment class
        if "Positive" in sentiment:
            sentiment_class = "positive"
        elif "Negative" in sentiment:
            sentiment_class = "negative"
        else:
            sentiment_class = "neutral"

        html_card = f"""
<div class="card">
    <div class="card-title">{title}</div>
    <p>Rating: {rating}</p>
    <p class="{sentiment_class}">{sentiment}</p>
    <p>{description}...</p>
</div>
"""

        st.markdown(html_card, unsafe_allow_html=True)
        
/* TITLE INSIDE CARD */
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
<h1>🎬 BingeWatch -- MoodWatch </h1>
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
