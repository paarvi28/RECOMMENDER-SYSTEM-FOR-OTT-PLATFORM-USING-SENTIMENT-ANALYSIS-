import streamlit as st
import pandas as pd

# ------------------ PAGE CONFIG ------------------ #
st.set_page_config(layout="wide")

# ------------------ GLOBAL STYLE ------------------ #
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}

h1, h2, h3, h4 {
    color: white;
}

.stTextInput>div>div>input {
    background-color: #1c1c1c;
    color: white;
}

.stSelectbox>div>div {
    background-color: #1c1c1c;
    color: white;
}

.block-container {
    padding-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------ #
st.title("🎬 BingeWatch - OTT Recommendation System")
st.markdown("Personalized recommendations using sentiment analysis")

# ------------------ LOAD DATA ------------------ #
try:
    df = pd.read_csv("final_movies.csv", encoding="latin1")
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# ------------------ CLEAN COLUMNS ------------------ #
df.columns = df.columns.str.lower().str.strip()

# ------------------ COLUMN MAPPING ------------------ #
title_col = next((c for c in df.columns if 'title' in c), df.columns[0])
genre_col = next((c for c in df.columns if 'listed' in c or 'genre' in c), None)
rating_col = next((c for c in df.columns if 'rating' in c or 'imdb' in c), None)
desc_col = next((c for c in df.columns if 'description' in c or 'overview' in c or 'summary' in c), None)

# ------------------ SENTIMENT FUNCTION ------------------ #
def get_sentiment(text):
    text = str(text).lower()

    pos = ['good','great','amazing','love','excellent','fun']
    neg = ['bad','boring','worst','hate','poor','slow']

    score = 0
    for w in pos:
        if w in text:
            score += 1
    for w in neg:
        if w in text:
            score -= 1

    if score > 0:
        return "😊 Positive"
    elif score < 0:
        return "😞 Negative"
    else:
        return "😐 Neutral"

# ------------------ APPLY SENTIMENT SAFELY ------------------ #
if desc_col and desc_col in df.columns:
    df['sentiment'] = df[desc_col].astype(str).apply(get_sentiment)
else:
    df['sentiment'] = "😐 Neutral"

# ------------------ SEARCH + FILTER UI ------------------ #
st.markdown("## 🔍 Discover Content")

col1, col2 = st.columns([2, 1])

with col1:
    search = st.text_input("Search movies or shows")

with col2:
    if genre_col:
        genres = sorted(df[genre_col].dropna().unique())
        selected_genre = st.selectbox("Genre", genres)
    else:
        selected_genre = None

# ------------------ FILTER LOGIC ------------------ #
filtered_df = df.copy()

if selected_genre and genre_col:
    filtered_df = filtered_df[
        filtered_df[genre_col].astype(str).str.contains(selected_genre, na=False)
    ]

if search:
    filtered_df = filtered_df[
        filtered_df[title_col].astype(str).str.contains(search, case=False, na=False)
    ]

filtered_df = filtered_df.head(20)

# ------------------ TRENDING SECTION ------------------ #
st.markdown("## 🔥 Trending Now")

trend_cols = st.columns(5)

for i, (_, row) in enumerate(filtered_df.head(5).iterrows()):
    with trend_cols[i]:
        st.image("https://via.placeholder.com/200x300.png?text=Trending", use_column_width=True)
        st.caption(row.get(title_col, "No Title"))

# ------------------ RECOMMENDED SECTION ------------------ #
st.markdown("## 🎬 Recommended For You")

cols = st.columns(4)

for i, row in filtered_df.iterrows():
    col = cols[i % 4]

    with col:
        title = row.get(title_col, "No Title")
        rating = row.get(rating_col, "N/A") if rating_col else "N/A"
        description = str(row.get(desc_col, "No description"))[:90] if desc_col else "No description"
        sentiment = row.get('sentiment', "😐 Neutral")

        # Sentiment badge
        if "Positive" in sentiment:
            badge = "🟢 Positive"
        elif "Negative" in sentiment:
            badge = "🔴 Negative"
        else:
            badge = "⚪ Neutral"

        # CARD UI (SAFE)
        with st.container():
            st.image("https://via.placeholder.com/300x400.png?text=Movie", use_column_width=True)
            st.markdown(f"**{title}**")
            st.caption(f"⭐ {rating}")
            st.write(badge)
            st.caption(description)

st.markdown("---")
st.caption("Built with ❤️ using Streamlit")
