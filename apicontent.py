from typing import List, Optional
from fastapi import FastAPI, Query
import snowflake.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

def fetch_movies_by_ids(content_type: str, unique_ids: Optional[List[str]] = None, name: Optional[str] = None):
    conn = snowflake.connector.connect(
        user=os.getenv('SF_USER'),
        password=os.getenv('SF_PASSWORD'),
        account=os.getenv('SF_ACCOUNT'),
        warehouse=os.getenv('SF_WAREHOUSE'),
        database=os.getenv('SF_DATABASE'),
        schema=os.getenv('SF_SCHEMA')
    )
    cursor = conn.cursor()
    try:
       table_name = "TRIAL_TABLE" if content_type == "movie" else "TV_TABLE"
       if unique_ids: # Create a parameterized query string with placeholders for unique_ids
        placeholders = ', '.join(['%s'] * len(unique_ids))
        query = f"""
            SELECT TITLE, DIRECTOR, CAST_MEMBER, RELEASE_YEAR, DURATION, AVAILABLE_ON, TRAILER, THUMBNAIL, UNIQUE_ID
            FROM {table_name}
            WHERE UNIQUE_ID IN ({placeholders})
        """.format(','.join(['%s' for _ in unique_ids]))  # Safe parameterization

        # Execute the query with the list of unique_ids
        cursor.execute(query, unique_ids)
       elif name:
            query = f"""
                SELECT TITLE, DIRECTOR, CAST_MEMBER, RELEASE_YEAR, DURATION, AVAILABLE_ON, TRAILER, THUMBNAIL, UNIQUE_ID
                FROM {table_name}
                WHERE LOWER(TITLE) LIKE LOWER(%s)
            """
            cursor.execute(query, (f"%{name}%",))
       else:
         return []
        
       result = cursor.fetchall()
       return result
    finally:
        cursor.close()
        conn.close()

@app.get("/content")
async def get_movies(content_type: str, unique_ids: Optional[List[str]] = Query(None), name: Optional[str] = Query(None)):
    if content_type not in ["movie", "tv_show"]:
        return {"error": "Invalid content type specified"}
    movie_data_list = fetch_movies_by_ids(content_type, unique_ids, name)    
    if movie_data_list:
        movies = []
        for movie_data in movie_data_list:
            movies.append({
                "title": movie_data[0],
                "director": movie_data[1],
                "cast_member": movie_data[2],
                "release_year": movie_data[3],
                "duration": movie_data[4],
                "available_on": movie_data[5],
                "trailer": movie_data[6] if movie_data[6] else "No trailer available" ,
                "thumbnail": movie_data[7] if movie_data[7] else "No thumbnail available",
                "unique_id": movie_data[8]
            })
        return movies
    else:
        return {"error": "No movies found"}
