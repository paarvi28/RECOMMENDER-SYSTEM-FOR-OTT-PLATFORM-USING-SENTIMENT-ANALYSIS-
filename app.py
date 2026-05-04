import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# ------------------ STYLE ------------------ #
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}

.block-container {
    padding-top: 1rem;
}

.card {
    background-color: #1c1c1c;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 20px;
    transition: transform 0.2s ease;
}

.card:hover {
    transform: scale(1.03);
}

.title {
    font-size:18px;
    font-weight:600;
}

.subtitle {
    color:gray;
    font-size:14px;
}

.badge-positive { color:#00ff88; font-weight:bold; }
.badge-negative { color:#ff4d4d; font-weight:bold; }
.badge-neutral { color:#cccccc; font-weight:bold; }
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------ #
st.title("🎬 BingeWatch")
st.markdown("Discover content based on **mood, genre & sentiment**")

# ------------------ LOAD DATA ------------------ #
try:
    df = pd.read_csv("final_movies.csv", encoding="latin1")
except:
    st.error("Dataset not found")
    st.stop()

df.columns = df.columns.str.lower()

title_col = 'title'
genre_col = 'listed_in'
rating_col = 'rating'
desc_col = 'description'

# ------------------ SENTIMENT ------------------ #
def get_sentiment(text):
    text = str(text).lower()
    pos = ['good','great','amazing','love','excellent','fun']
    neg = ['bad','boring','worst','hate','poor','slow']

    score = 0
    for w in pos:
        if w in text: score += 1
    for w in neg:
        if w in text: score -= 1

    if score > 0: return "Positive"
    elif score < 0: return "Negative"
    else: return "Neutral"

if desc_col:
    df['sentiment'] = df[desc_col].astype(str).apply(get_sentiment)
else:
    df['sentiment'] = "Neutral"

# ------------------ FILTER BAR ------------------ #
col1, col2, col3 = st.columns([2,2,1])

with col1:
    search = st.text_input("🔍 Search movie/show")

with col2:
    genres = df[genre_col].dropna().unique()
    selected_genre = st.selectbox("🎭 Genre", genres)

with col3:
    min_rating = st.slider("⭐ Rating", 0.0, 10.0, 5.0)

# ------------------ FILTER LOGIC ------------------ #
filtered_df = df.copy()

if search:
    filtered_df = filtered_df[filtered_df[title_col].str.contains(search, case=False, na=False)]

if selected_genre:
    filtered_df = filtered_df[filtered_df[genre_col].str.contains(selected_genre, na=False)]

if rating_col in df.columns:
    filtered_df = filtered_df[pd.to_numeric(filtered_df[rating_col], errors='coerce') >= min_rating]

filtered_df = filtered_df.head(20)

# ------------------ TRENDING ROW ------------------ #
st.subheader("🔥 Trending Now")

scroll_html = "<div style='display:flex; overflow-x:auto;'>"

for _, row in filtered_df.head(10).iterrows():
    scroll_html += f"""
    <div style="min-width:200px; margin-right:15px;">
        <div class="card">
            <div class="title">{row[title_col]}</div>
            <div class="subtitle">⭐ {row.get(rating_col, 'N/A')}</div>
        </div>
    </div>
    """

scroll_html += "</div>"

st.markdown(scroll_html, unsafe_allow_html=True)

# ------------------ GRID CARDS ------------------ #
st.subheader("🎯 Recommended for You")

cols = st.columns(4)

for i, row in filtered_df.iterrows():
    col = cols[i % 4]

    sentiment = row['sentiment']
    if sentiment == "Positive":
        badge = "badge-positive"
    elif sentiment == "Negative":
        badge = "badge-negative"
    else:
        badge = "badge-neutral"

    with col:
        st.markdown(f"""
        <div class="card">
            <div class="title">{row[title_col]}</div>
            <div class="subtitle">⭐ {row.get(rating_col, 'N/A')}</div>
            <div class="{badge}">{sentiment}</div>
            <div class="subtitle">{str(row[desc_col])[:100]}...</div>
        </div>
        """, unsafe_allow_html=True)
