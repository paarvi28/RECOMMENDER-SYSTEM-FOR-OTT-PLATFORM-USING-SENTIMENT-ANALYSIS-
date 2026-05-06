import streamlit as st
import pandas as pd

# ------------------ PAGE CONFIG ------------------ #
st.set_page_config(layout="wide")

# ------------------ TITLE ------------------ #
st.title("🎬 BingeWatch - OTT Recommendation System")
st.markdown("Personalized recommendations using sentiment analysis")

# ------------------ HERO SECTION ------------------ #
st.markdown("""
<div style="
    background: linear-gradient(to right, #000000, #1f1f1f);
    padding: 30px;
    border-radius: 12px;
    margin-bottom: 20px;
">
    <h1 style="color:white;">🎬 Welcome to BingeWatch</h1>
    <p style="color:#ccc;">
    Discover movies based on mood, genre, and sentiment intelligence.
    </p>
</div>
""", unsafe_allow_html=True)

# ------------------ LOAD DATA ------------------ #
try:
    df = pd.read_csv("final_movies.csv", encoding="latin1")
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# ------------------ CLEAN COLUMNS ------------------ #
df.columns = df.columns.str.lower().str.strip()

# Auto-detect columns safely
title_col = next((c for c in df.columns if 'title' in c), df.columns[0])
genre_col = next((c for c in df.columns if 'listed' in c or 'genre' in c), None)
rating_col = next((c for c in df.columns if 'rating' in c or 'imdb' in c), None)
desc_col = next((c for c in df.columns if 'description' in c or 'overview' in c), None)

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

# Apply sentiment safely
if desc_col and desc_col in df.columns:
    df['sentiment'] = df[desc_col].astype(str).apply(get_sentiment)
else:
    df['sentiment'] = "😐 Neutral"

# ------------------ FILTER ------------------ #
st.subheader("🎯 Filter Content")

if genre_col:
    genres = df[genre_col].dropna().unique()
    selected_genre = st.selectbox("Select Genre", genres)

    filtered_df = df[df[genre_col].astype(str).str.contains(selected_genre, na=False)].head(20)
else:
    filtered_df = df.head(20)

# ------------------ STYLE ------------------ #
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
</style>
""", unsafe_allow_html=True)

# ------------------ TRENDING SCROLL ------------------ #
st.subheader("🔥 Trending Now")

scroll_html = "<div style='display:flex; overflow-x:auto;'>"

for _, row in filtered_df.head(10).iterrows():
    scroll_html += f"""
    <div style="min-width:200px; margin-right:15px;">
        <div style="
            background:#1c1c1c;
            padding:10px;
            border-radius:10px;
        ">
            <p style="color:white;">{row.get(title_col, 'No Title')}</p>
        </div>
    </div>
    """

scroll_html += "</div>"
st.markdown(scroll_html, unsafe_allow_html=True)

# ------------------ POSTER PLACEHOLDER ------------------ #
def get_dummy_poster():
    return "https://via.placeholder.com/300x450.png?text=No+Image"

# ------------------ RECOMMENDED CARDS ------------------ #
st.subheader("🔥 Recommended for You")

cols = st.columns(3)

for i, row in filtered_df.iterrows():
    col = cols[i % 3]

    with col:
        title = row.get(title_col, "No Title")
        rating = row.get(rating_col, "N/A") if rating_col else "N/A"
        description = str(row.get(desc_col, "No description")) if desc_col else "No description"
        sentiment = row.get('sentiment', "😐 Neutral")

        # Sentiment color
        if "Positive" in sentiment:
            color = "#00ff88"
        elif "Negative" in sentiment:
            color = "#ff4d4d"
        else:
            color = "#cccccc"

        st.markdown(f"""
        <div style="
            background-color:#141414;
            border-radius:12px;
            overflow:hidden;
            margin-bottom:20px;
            box-shadow:0 6px 15px rgba(0,0,0,0.6);
        ">
            <img src="{get_dummy_poster()}" style="width:100%; height:300px; object-fit:cover;">
            
            <div style="padding:10px;">
                <h4 style="color:white; margin-bottom:5px;">{title}</h4>
                
                <p style="color:#aaa; font-size:13px;">
                    ⭐ {rating}
                </p>

                <p style="color:{color}; font-weight:bold;">
                    {sentiment}
                </p>

                <p style="color:#bbb; font-size:12px;">
                    {description[:90]}...
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
