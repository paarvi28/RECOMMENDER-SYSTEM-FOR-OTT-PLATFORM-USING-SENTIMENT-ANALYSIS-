import streamlit as st
import pandas as pd
import requests
import random

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="BingeWatch OTT",
    page_icon="🎬",
    layout="wide"
)

TMDB_API_KEY = "11da9eae256550559571dda4eb783d7c"

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>

/* GOOGLE FONT */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

/* FULL PAGE */
html, body, .stApp {
    background: linear-gradient(135deg, #0b1120, #111827, #020617);
    color: white;
    font-family: 'Poppins', sans-serif;
}

/* REMOVE STREAMLIT DEFAULTS */
header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

/* MAIN CONTAINER */
.block-container {
    padding-top: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* HERO SECTION */
.hero {
    background: linear-gradient(90deg, rgba(15,23,42,0.95), rgba(30,41,59,0.7)),
                url('https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=2070&auto=format&fit=crop');
    background-size: cover;
    background-position: center;
    border-radius: 20px;
    padding: 60px;
    margin-bottom: 30px;
    box-shadow: 0px 8px 30px rgba(0,0,0,0.5);
}

/* TITLES */
.hero-title {
    font-size: 52px;
    font-weight: 700;
    background: linear-gradient(90deg, #818cf8, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #d1d5db;
    font-size: 18px;
    margin-top: 10px;
}

/* SEARCH INPUT */
.stTextInput input {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid #334155 !important;
    padding: 10px !important;
}

/* SELECT BOX */
.stSelectbox div[data-baseweb="select"] {
    background-color: #1e293b !important;
    border-radius: 12px !important;
    color: white !important;
}

/* CARD */
.movie-card {
    background: rgba(30, 41, 59, 0.6);
    backdrop-filter: blur(10px);
    border-radius: 18px;
    padding: 12px;
    transition: 0.3s ease;
    border: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 20px;
}

.movie-card:hover {
    transform: scale(1.03);
    box-shadow: 0px 10px 25px rgba(99,102,241,0.3);
}

/* MOVIE TITLE */
.movie-title {
    font-size: 17px;
    font-weight: 600;
    color: #f8fafc;
    margin-top: 10px;
}

/* MOVIE DESCRIPTION */
.movie-desc {
    font-size: 13px;
    color: #cbd5e1;
}

/* SENTIMENT */
.positive {
    color: #22c55e;
    font-weight: 600;
}

.negative {
    color: #ef4444;
    font-weight: 600;
}

.neutral {
    color: #94a3b8;
    font-weight: 600;
}

/* SECTION TITLES */
.section-title {
    font-size: 28px;
    font-weight: 600;
    color: white;
    margin-top: 10px;
    margin-bottom: 15px;
}

 /* SIDEBAR BACKGROUND */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #141E30 0%,
        #243B55 100%
    );
    border-right: 2px solid #E50914;
}

/* SIDEBAR TEXT */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* NAVIGATION TITLE */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #E50914 !important;
    font-weight: bold;
}

/* RADIO BUTTON LABELS */
.stRadio label {
    color: white !important;
    font-size: 16px !important;
}

/* SIDEBAR HOVER EFFECT */
section[data-testid="stSidebar"] .stRadio label:hover {
    color: #E50914 !important;
    transition: 0.3s;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HERO SECTION
# ---------------------------------------------------
st.markdown("""
<style>

/* NETFLIX TITLE ANIMATION */
@keyframes fadeSlide {
    0% {
        opacity: 0;
        transform: translateY(-40px) scale(0.9);
        letter-spacing: 8px;
    }

    100% {
        opacity: 1;
        transform: translateY(0px) scale(1);
        letter-spacing: 1px;
    }
}

/* MAIN TITLE */
.netflix-title {
    font-family: Poppins,  'Poppins', sans-serif;
    font-size: 64px;
    color: #E50914;
    text-align: center;
    font-weight: 900;
    margin-top: 10px;
    margin-bottom: 0px;
    animation: fadeSlide 2.5s ease;
    text-shadow:
        0 0 10px rgba(229,9,20),
        0 0 20px rgba(229,9,20);
}

/* SUBTITLE */
.netflix-subtitle {
    text-align: center;
    color: #d1d5db;
    font-size: 22px;
    margin-top: -10px;
    margin-bottom: 35px;
    font-family: 'Poppins', sans-serif;
    animation: fadeSlide 2.5s ease;
}

</style>

<div class="netflix-title">
🎬 BingeWatch -- MoodWatch
</div>

<div class="netflix-subtitle">
Your AI-powered OTT Recommendation Engine
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

if "liked_movies" not in st.session_state:
    st.session_state.liked_movies = []

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
try:
    df = pd.read_csv("final_movies.csv", encoding="latin1")
except:
    st.error("Dataset not found. Please check final_movies.csv")
    st.stop()

df.columns = df.columns.str.lower()

title_col = next((c for c in df.columns if 'title' in c), df.columns[0])
genre_col = next((c for c in df.columns if 'listed' in c or 'genre' in c), None)
desc_col = next((c for c in df.columns if 'description' in c or 'overview' in c), None)

# ---------------------------------------------------
# SENTIMENT ANALYSIS
# ---------------------------------------------------
def get_sentiment(text):

    text = str(text).lower()

    positive_words = [
        'good', 'great', 'amazing', 'love',
        'excellent', 'fun', 'best', 'awesome'
    ]

    negative_words = [
        'bad', 'boring', 'worst',
        'hate', 'poor', 'slow'
    ]

    score = 0

    for word in positive_words:
        if word in text:
            score += 1

    for word in negative_words:
        if word in text:
            score -= 1

    if score > 0:
        return "🟢 Positive"

    elif score < 0:
        return "🔴 Negative"

    return "⚪ Neutral"

if desc_col:
    df["sentiment"] = df[desc_col].astype(str).apply(get_sentiment)
else:
    df["sentiment"] = "⚪ Neutral"

# ---------------------------------------------------
# TMDB FUNCTION
# ---------------------------------------------------
@st.cache_data(show_spinner=False)
def get_movie_data(title):

    try:

        search_url = (
            f"https://api.themoviedb.org/3/search/movie"
            f"?api_key={TMDB_API_KEY}&query={title}"
        )

        response = requests.get(search_url).json()

        if response.get("results"):

            movie = response["results"][0]

            poster = movie.get("poster_path")
            movie_id = movie.get("id")

            poster_url = (
                f"https://image.tmdb.org/t/p/w500{poster}"
                if poster else None
            )

            trailer_url = None

            if movie_id:

                videos = requests.get(
                    f"https://api.themoviedb.org/3/movie/{movie_id}/videos"
                    f"?api_key={TMDB_API_KEY}"
                ).json()

                for video in videos.get("results", []):

                    if video.get("type") == "Trailer":

                        trailer_url = (
                            f"https://www.youtube.com/watch?v={video['key']}"
                        )

                        break

            return poster_url, trailer_url

    except:
        return None, None

    return None, None

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.title("🎥 Navigation")

page = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "❤️ Watchlist"]
)

# ---------------------------------------------------
# HOME PAGE
# ---------------------------------------------------
if page == "🏠 Home":

    st.markdown(
        '<div class="section-title">🔍 Discover Content</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        search = st.text_input(
            "Search Movies or Shows"
        )

    with col2:

        if genre_col:

            genres = sorted(
                list(df[genre_col].dropna().astype(str).unique())
            )

            selected_genre = st.selectbox(
                "Select Genre",
                ["All"] + genres
            )

        else:
            selected_genre = "All"

    filtered_df = df.copy()

    if selected_genre != "All" and genre_col:

        filtered_df = filtered_df[
            filtered_df[genre_col]
            .astype(str)
            .str.contains(selected_genre, case=False, na=False)
        ]

    if search:

        filtered_df = filtered_df[
            filtered_df[title_col]
            .astype(str)
            .str.contains(search, case=False, na=False)
        ]

    filtered_df = filtered_df.head(16)

    # ---------------------------------------------------
    # TRENDING ROW
    # ---------------------------------------------------
    st.markdown(
        '<div class="section-title">🔥 Trending Now</div>',
        unsafe_allow_html=True
    )

    trending = st.columns(6)

    for i, (_, row) in enumerate(filtered_df.head(6).iterrows()):

        with trending[i]:

            poster, _ = get_movie_data(row[title_col])

            st.image(
                poster if poster else
                "https://via.placeholder.com/200x300",
                use_container_width=True
            )

    # ---------------------------------------------------
    # MAIN GRID
    # ---------------------------------------------------
    st.markdown(
        '<div class="section-title">🎬 Recommended For You</div>',
        unsafe_allow_html=True
    )

    cols = st.columns(4)

    for i, (_, row) in enumerate(filtered_df.iterrows()):

        with cols[i % 4]:

            title = row.get(title_col, "No Title")
            sentiment = row.get("sentiment", "⚪ Neutral")

            description = (
                str(row.get(desc_col, "No description"))[:100]
                if desc_col else "No description"
            )

            poster, trailer = get_movie_data(title)

            # sentiment color
            if "Positive" in sentiment:
                sentiment_class = "positive"

            elif "Negative" in sentiment:
                sentiment_class = "negative"

            else:
                sentiment_class = "neutral"

            st.markdown(
                '<div class="movie-card">',
                unsafe_allow_html=True
            )

            st.image(
                poster if poster else
                "https://via.placeholder.com/300x400",
                use_container_width=True
            )

            st.markdown(
                f'<div class="movie-title">{title}</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="{sentiment_class}">{sentiment}</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="movie-desc">{description}...</div>',
                unsafe_allow_html=True
            )

            # buttons
            b1, b2 = st.columns(2)

            with b1:

                if st.button(
                    "❤️ Like",
                    key=f"like_{i}"
                ):

                    if title not in st.session_state.watchlist:

                        st.session_state.watchlist.append(title)

                        st.success("Added to Watchlist")

            with b2:

                if trailer:

                    with st.popover("▶ Trailer"):
                        st.video(trailer)

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

# ---------------------------------------------------
# WATCHLIST PAGE
# ---------------------------------------------------
elif page == "❤️ Watchlist":

    st.markdown(
        '<div class="section-title">❤️ Your Watchlist</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.watchlist:

        st.info("No movies added yet.")

    else:

        for movie in st.session_state.watchlist:

            st.write(f"• {movie}")
