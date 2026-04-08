import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import os


def sf_upload(csv1,csv2):
# Set up the connection to Snowflake
    ctx = snowflake.connector.connect(
        user=os.getenv('SF_USER'),
        password=os.getenv('SF_PASSWORD'),
        account=os.getenv('SF_ACCOUNT'),
        warehouse=os.getenv('SF_WAREHOUSE'),
        database=os.getenv('SF_DATABASE'),
        schema=os.getenv('SF_SCHEMA')
    )

    cur = ctx.cursor()

    try:
        # Optionally create a table to store CSV data
        create_table_query = """
        CREATE TABLE IF NOT EXISTS MOVIE_TABLE (
            TYPE VARCHAR(16777216),
            TITLE VARCHAR(16777216),
            DIRECTOR VARCHAR(16777216),
            CAST_MEMBER VARCHAR(16777216),
            COUNTRY VARCHAR(16777216),
            DATE_ADDED VARCHAR(16777216),
            RELEASE_YEAR NUMBER(38,0),
            RATING VARCHAR(16777216),
            DURATION VARCHAR(16777216),
            LISTED_IN VARCHAR(16777216),
            DESCRIPTION VARCHAR(16777216),
            AVAILABLE_ON VARCHAR(16777216),
            TRAILER VARCHAR(16777216),
            THUMBNAIL VARCHAR(16777216),
            KEYWORDS VARCHAR(16777216),
            SENTENCES VARCHAR(16777216),
            UNIQUE_ID VARCHAR(16777216)
        );
        """
        cur.execute(create_table_query)

        # Load CSV file into DataFrame
        file_path = (csv1)
        df1 = pd.read_csv(file_path)

        # Rename DataFrame columns to match the Snowflake table's column names exactly
        # Assuming your CSV has columns like 'movie_type', 'movie_title', etc.
        column_mapping = {
            'type': 'TYPE',
            'title': 'TITLE', 
            'director': 'DIRECTOR',
            'cast': 'CAST_MEMBER',
            'country': 'COUNTRY', 
            'date_added': 'DATE_ADDED',
            'release_year': 'RELEASE_YEAR', 
            'rating': 'RATING', 
            'duration': 'DURATION', 
            'listed_in': 'LISTED_IN', 
            'description': 'DESCRIPTION',
            'available_on': 'AVAILABLE_ON', 
            'trailer':'TRAILER', 
            'thumbnail':'THUMBNAIL', 
            'keywords': 'KEYWORDS', 
            'sentences':'SENTENCES',
            'unique_id': 'UNIQUE_ID'
            
            
            # Add all necessary mappings
        }
        df1.rename(columns=column_mapping, inplace=True)

        # Verify that column names match exactly
        print("DataFrame columns:", df1.columns)
        
        # Use the built-in function to write data from DataFrame to Snowflake
        write_pandas(ctx, df1, 'MOVIE_TABLE')
    except Exception as e:
        print(f"Failed in {e}")  
        return     

    try:
        # Optionally create a table to store CSV data
        create_table_query = """
        CREATE TABLE IF NOT EXISTS TV_TABLE (
            TYPE VARCHAR(16777216),
            TITLE VARCHAR(16777216),
            DIRECTOR VARCHAR(16777216),
            CAST_MEMBER VARCHAR(16777216),
            COUNTRY VARCHAR(16777216),
            DATE_ADDED VARCHAR(16777216),
            RELEASE_YEAR NUMBER(38,0),
            RATING VARCHAR(16777216),
            DURATION VARCHAR(16777216),
            LISTED_IN VARCHAR(16777216),
            DESCRIPTION VARCHAR(16777216),
            AVAILABLE_ON VARCHAR(16777216),
            TRAILER VARCHAR(16777216),
            THUMBNAIL VARCHAR(16777216),
            KEYWORDS VARCHAR(16777216),
            SENTENCES VARCHAR(16777216),
            UNIQUE_ID VARCHAR(16777216)
        );
        """
        cur.execute(create_table_query)

        # Load CSV file into DataFrame
        file_path = (csv2)
        df2 = pd.read_csv(file_path)

        # Rename DataFrame columns to match the Snowflake table's column names exactly
        # Assuming your CSV has columns like 'movie_type', 'movie_title', etc.
        column_mapping = {
            'type': 'TYPE',
            'title': 'TITLE', 
            'director': 'DIRECTOR',
            'cast': 'CAST_MEMBER',
            'country': 'COUNTRY', 
            'date_added': 'DATE_ADDED',
            'release_year': 'RELEASE_YEAR', 
            'rating': 'RATING', 
            'duration': 'DURATION', 
            'listed_in': 'LISTED_IN', 
            'description': 'DESCRIPTION',
            'available_on': 'AVAILABLE_ON', 
            'trailer':'TRAILER', 
            'thumbnail':'THUMBNAIL', 
            'keywords': 'KEYWORDS', 
            'sentences':'SENTENCES',
            'unique_id': 'UNIQUE_ID'
            
            
            # Add all necessary mappings
        }
        df2.rename(columns=column_mapping, inplace=True)

        # Verify that column names match exactly
        print("DataFrame columns:", df2.columns)
        
        # Use the built-in function to write data from DataFrame to Snowflake
        write_pandas(ctx, df1, 'TV_TABLE')


    finally:
        cur.close()
        ctx.close()
