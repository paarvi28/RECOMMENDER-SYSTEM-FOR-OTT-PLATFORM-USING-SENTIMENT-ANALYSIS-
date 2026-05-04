import streamlit as st
import pandas as pd

st.title("🎬 BingeWatch Recommendation System")

try:
    df = pd.read_csv("MoviesOnStreamingPlatforms.csv")
except:
    st.error("Dataset not found. Please check path.")
    st.stop()

genre = st.selectbox("Select Genre", df['listed_in'].dropna().unique())

filtered = df[df['listed_in'].str.contains(genre, na=False)]

st.subheader("Recommended Content:")
st.write(filtered[['title', 'description']].head(10))

try:
    
    st.success("Dataset loaded successfully!")
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()
