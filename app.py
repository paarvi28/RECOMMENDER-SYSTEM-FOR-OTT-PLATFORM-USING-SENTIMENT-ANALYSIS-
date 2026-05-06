import streamlit as st
import pandas as pd

# Page config
st.set_page_config(layout="wide")

# Title
st.title("🎬 BingeWatch - OTT Recommendation System")
st.markdown("Personalized recommendations using sentiment analysis")

# ------------------ LOAD DATA ------------------ #
try:
    df = pd.read_csv("final_movies.csv", encoding="latin1")
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# Standardize column names
df.columns = df.columns.str.lower()

# ------------------ COLUMN MAPPING ------------------ #
title_col = 'title' if 'title' in df.columns else df.columns[0]
genre_col = 'listed_in' if 'listed_in' in df.columns else None
rating_col = 'rating' if 'rating' in df.columns else None
desc_col = 'description' if 'description' in df.columns else None

# ------------------ SENTIMENT FUNCTION ------------------ #
def get_sentiment(text):
    text = str(text).lower()

    positive_words = ['good', 'great', 'amazing', 'love', 'excellent', 'fun']
    negative_words = ['bad', 'boring', 'worst', 'hate', 'poor', 'slow']

    score = 0
    for word in positive_words:
        if word in text:
            score += 1
    for word in negative_words:
        if word in text:
            score -= 1

    if score > 0:
        return "😊 Positive"
    elif score < 0:
        return "😞 Negative"
    else:
        return "😐 Neutral"

# Apply sentiment
if desc_col:
    df['sentiment'] = df[desc_col].apply(get_sentiment)
else:
    df['sentiment'] = "😐 Neutral"

# ------------------ FILTER ------------------ #
st.subheader("🎯 Filter Content")

if genre_col:
    genres = df[genre_col].dropna().unique()
    selected_genre = st.selectbox("Select Genre", genres)

    filtered_df = df[df[genre_col].astype(str).str.contains(selected_genre, na=False)].head(12)
else:
    filtered_df = df.head(12)

# ------------------ STYLE ------------------ #
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
</style>
""", unsafe_allow_html=True)

# ------------------ NETFLIX STYLE CARDS ------------------ #
st.subheader("🔥 Recommended for You")

cols = st.columns(3)

for i, row in filtered_df.iterrows():
    col = cols[i % 3]

    with col:
        title = row.get(title_col, "No Title")
        rating = row.get(rating_col, "N/A") if rating_col else "N/A"
        description = str(row.get(desc_col, "No description"))[:120] if desc_col else "No description"
        sentiment = row.get('sentiment', "😐 Neutral")

        # Sentiment color
        if "Positive" in sentiment:
            color = "#00ff00"
        elif "Negative" in sentiment:
            color = "#ff4d4d"
        else:
            color = "#cccccc"

        st.markdown(f"""
        <div style="
            background-color:#1c1c1c;
            padding:12px;
            border-radius:10px;
            margin-bottom:20px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.5);
        ">
            <h4 style="color:white;">{title}</h4>
            <p style="color:gray;">⭐ {rating}</p>
            <p style="color:{color};">{sentiment}</p>
            <p style="color:#bbb;">{description}...</p>
        </div>
        """, unsafe_allow_html=True)
