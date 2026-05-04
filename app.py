import os
import streamlit as st
import pandas as pd

st.title("🎬 BingeWatch Recommendation System")

# Load dataset
try:
    df = pd.read_csv("final_movies.csv")
    st.success("Dataset loaded successfully!")
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()
