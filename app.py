import os
import streamlit as st
import pandas as pd

st.title("🎬 BingeWatch Recommendation System")
st.markdown("Personalized recommendations using sentiment analysis")

# Load dataset
try:
    df = pd.read_csv("final_movies.csv")
    st.success("Dataset loaded successfully!")
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

from textblob import TextBlob

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
df['sentiment'] = df['overview'].apply(get_sentiment)

st.markdown(
    f"""
    <p style="color:#00ffcc;">{row['sentiment']}</p>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<style>
body {
    background-color: #0e1117;
}
</style>
""", unsafe_allow_html=True)
cols = st.columns(3)

for i, row in filtered_df.iterrows():
    col = cols[i % 3]

    with col:
        st.markdown(f"""
        <div style="
            background-color:#1c1c1c;
            padding:10px;
            border-radius:10px;
            margin-bottom:20px;
        ">
            <h4 style="color:white;">{row['title']}</h4>
            <p style="color:gray;">⭐ {row.get('imdb', 'N/A')}</p>
            <p style="color:#bbb;">{str(row.get('overview', 'No description'))[:100]}...</p>
        </div>
        """, unsafe_allow_html=True)
