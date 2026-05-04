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
    polarity = TextBlob(str(text)).sentiment.polarity
    if polarity > 0.1:
        return "😊 Positive"
    elif polarity < -0.1:
        return "😞 Negative"
    else:
        return "😐 Neutral"

df['sentiment'] = df['overview'].apply(get_sentiment)

<p style="color:#00ffcc;">{row['sentiment']}</p>

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
