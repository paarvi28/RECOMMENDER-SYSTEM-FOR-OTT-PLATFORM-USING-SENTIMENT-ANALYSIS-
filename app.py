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
header, footer, #MainMenu {
    visibility: hidden;
}

/* MAIN CONTAINER */
.block-container {
    padding-top: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #141E30 0%,
        #243B55 100%
    );
    border-right: 2px solid #E50914;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #E50914 !important;
    font-weight: bold;
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

/* MOVIE CARD */
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
    font-size: 18px;
    font-weight: 600;
    color: #f8fafc;
    margin-top: 10px;
}

/* DESCRIPTION */
.movie-desc {
    font-size: 13px;
    color: #cbd5e1;
}

/* SENTIMENT COLORS */
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

/* TITLE ANIMATION */
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
    font-size: 64px;
    color: #E50914;
    text-align: center;
    font-weight: 900;
    margin-top: 10px;
    margin-bottom: 0px;
    animation: fadeSlide 2.5s ease;
    text-shadow:
        0 0 10px rgba(229,9,20,0.8),
        0 0 20px rgba(229,9,20,0.5);
}

/* SUBTITLE */
.netflix-subtitle {
    text-align: center;
    color: #d1d5db;
    font-size: 22px;
    margin-top: -10px;
    margin-bottom: 35px;
    animation: fadeSlide 2.5s ease;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HERO TITLE
# ---------------------------------------------------
st.markdown("""
<div class="netflix-title">
🎬 BingeWatch -- MoodWatch
</div>

<div class="netflix-subtitle">
Your AI-powered OTT Recommendation Engine
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

if "positive_feedback" not in st.session_state:
    st.session_state.positive_feedback = 0

if "negative_feedback" not in st.session_state:
    st.session_state.negative_feedback = 0
# LOAD DATA
# ---------------------------------------------------
try:
    df = pd.read_csv("final_movies.csv", encoding="latin1")
except Exception:
    st.error("Dataset not found. Please check final_movies.csv")
    st.stop()

df.columns = df.columns.str.lower()

title_col = next((c for c in df.columns if 'title' in c), df.columns[0])

genre_col = next(
    (c for c in df.columns if 'listed' in c or 'genre' in c),
    None
)

desc_col = next(
    (c for c in df.columns if 'description' in c or 'overview' in c),
    None
)

# ---------------------------------------------------
# SENTIMENT ANALYSIS
# ---------------------------------------------------
def get_sentiment(text):

    text = str(text).lower()

    positive_words = [
        'good', 'great', 'amazing', 'love',
        'excellent', 'fun', 'best',
        'awesome', 'fantastic', 'masterpiece'
    ]

    negative_words = [
        'bad', 'boring', 'worst',
        'hate', 'poor', 'slow',
        'awful', 'terrible'
    ]

    score = 0

    for word in positive_words:
        if word in text:
            score += 1

    for word in negative_words:
        if word in text:
            score -= 1

    final_score = max(min(score * 20, 100), -100)

    if final_score > 20:
        sentiment = "🟢 Positive"

    elif final_score < -20:
        sentiment = "🔴 Negative"

    else:
        sentiment = "⚪ Neutral"

    return sentiment, final_score

# SAFE DESCRIPTION CHECK
if desc_col:
    df[["sentiment", "sentiment_score"]] = df[desc_col].apply(
        lambda x: pd.Series(get_sentiment(x))
    )
else:
    df["sentiment"] = "⚪ Neutral"
    df["sentiment_score"] = 0

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

    except Exception:
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
        search = st.text_input("Search Movies or Shows")

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

    # FILTERING
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
    # METRICS
    # ---------------------------------------------------
    positive_count = (
    df["sentiment"].str.contains("Positive").sum()
    + st.session_state.positive_feedback
    )

    negative_count = (
    df["sentiment"].str.contains("Negative").sum()
    + st.session_state.negative_feedback
    )

    neutral_count = (
    df["sentiment"].str.contains("Neutral").sum()
    )

    a1, a2, a3 = st.columns(3)

    with a1:
        st.metric("🟢 Positive Content", positive_count)

    with a2:
        st.metric("🔴 Negative Content", negative_count)

    with a3:
        st.metric("⚪ Neutral Content", neutral_count)

    # ---------------------------------------------------
    # TRENDING
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
            score = row.get("sentiment_score", 0)

            description = (
                str(row.get(desc_col, "No description"))[:100]
                if desc_col else "No description"
            )

            poster, trailer = get_movie_data(title)

            # SENTIMENT CLASS
            if "Positive" in sentiment:
                sentiment_class = "positive"

            elif "Negative" in sentiment:
                sentiment_class = "negative"

            else:
                sentiment_class = "neutral"

            # CARD START
            st.markdown(
                '<div class="movie-card">',
                unsafe_allow_html=True
            )

            # IMAGE
            st.image(
                poster if poster else
                "https://via.placeholder.com/300x400",
                use_container_width=True
            )

            # TITLE
            st.markdown(
                f'<div class="movie-title">{title}</div>',
                unsafe_allow_html=True
            )

            # SENTIMENT
            st.markdown(
                f'<div class="{sentiment_class}">{sentiment}</div>',
                unsafe_allow_html=True
            )

            # SENTIMENT BAR
            st.progress((score + 100) / 200)

            # SCORE
            st.caption(f"Sentiment Score: {score}")

            # DESCRIPTION
            st.markdown(
                f'<div class="movie-desc">{description}...</div>',
                unsafe_allow_html=True
            )

            # BUTTONS
            b1, b2 = st.columns(2)

            with b1:

                if st.button(
                    "❤️ Like",
                    key=f"like_{i}"
                ):

                    if title not in st.session_state.watchlist:

                        st.session_state.watchlist.append(title)

                        st.success("Added to Watchlist")

                    else:
                        st.info("Already in Watchlist")

            with b2:

                if trailer:

                    with st.popover("▶ Trailer"):

                        st.video(trailer)

            # FEEDBACK BUTTONS
# FEEDBACK BUTTONS
f1, f2 = st.columns(2)

with f1:

    if st.button(
        "👍",
        key=f"feedback_like_{i}"
    ):

        st.session_state.positive_feedback += 1

        st.success("Thanks for your feedback!")

        st.rerun()

with f2:

    if st.button(
        "👎",
        key=f"feedback_dislike_{i}"
    ):

        st.session_state.negative_feedback += 1

        st.warning("Feedback noted!")

        st.rerun()

        
            # CARD END
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
