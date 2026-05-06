from fastapi import FastAPI
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load dataset
df = pd.read_csv("final_movies.csv", encoding="latin1")
df.columns = df.columns.str.lower()

@app.get("/")
def home():
    return {"message": "BingeWatch API running"}

@app.get("/recommend")
def recommend(query: str = ""):
    if query:
        results = df[df['title'].str.contains(query, case=False, na=False)].head(10)
    else:
        results = df.head(10)

    return results.to_dict(orient="records")
