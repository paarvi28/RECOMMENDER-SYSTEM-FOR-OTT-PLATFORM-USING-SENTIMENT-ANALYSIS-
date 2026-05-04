import os
import streamlit as st
import pandas as pd

st.title("🎬 BingeWatch Recommendation System")

st.write("Current files in directory:")
st.write(os.listdir())

try:
    df = pd.read_csv("MoviesOnStreamingPlatforms.csv")
    st.success("Dataset loaded successfully!")
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()
