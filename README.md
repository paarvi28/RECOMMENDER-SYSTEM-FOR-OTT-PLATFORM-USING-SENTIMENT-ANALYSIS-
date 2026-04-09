# RECOMMENDER-SYSTEM-FOR-OTT-PLATFORM-USING-SENTIMENT-ANALYSIS-
_**OVERVIEW**_

Binge Watch is a smart recommendation system designed to make content discovery easier across various OTT streaming platforms. With so much digital entertainment available, users often struggle to find relevant and engaging content. This project aims to solve that problem by providing a clear and organized way to offer personalized recommendations.
Binge Watch uses data-driven methods and machine learning to analyze user preferences, content details, and contextual clues. By adding filters like genre, mood, and viewing context (for instance, casual watching, family time, or binge sessions), the system offers recommendations that are both personalized and relevant to the situation.
In addition to basic filtering, the platform has semantic understanding and similarity-based retrieval methods to give more detailed recommendations. It examines content descriptions, keywords, and user behavior to find hidden connections between items. Techniques such as vector-based similarity search and retrieval-augmented generation (RAG) improve the system’s ability to provide meaningful and varied suggestions.
From a design perspective, the system is built as a complete data pipeline, which includes:
- Data Ingestion: Collecting content data from various sources, including APIs and curated datasets
- Data Processing: Cleaning, transforming, and creating features using scalable ETL workflows
- Storage & Indexing: Efficient storage of structured data and vector embeddings for quick retrieval
- Recommendation Engine: A mixed approach that combines rule-based filtering and similarity search
- API & Interface Layer: Smooth interaction through backend services and a user-friendly frontend
The use of workflow orchestration tools ensures dependable scheduling and execution of data pipelines, while containerization allows for portability and consistency across development and deployment environments.

The main goals of Binge-watch are to:
- Provide highly personalized and context-aware recommendations
- Decrease user decision fatigue through smart content curation
- Ensure scalability to manage increasing datasets and user interactions
- Show a practical approach to building recommendation systems
This project demonstrates a real-world application of data engineering, machine learning, and system design concepts, offering a practical solution to modern recommendation challenges. It improves user experience and serves as a strong example of how to build scalable AI-driven applications.

_**SYSTEM OBJECTIVES**_

The primary objectives of BingeWatch include:
- Delivering highly personalized and context-aware recommendations
- Reducing user decision fatigue through intelligent content curation
- Ensuring scalability to handle growing datasets and user interactions
- Demonstrating a production-oriented approach to building recommendation systems 

_**SIGNIFICANCE**_

This project reflects a practical implementation of concepts from data engineering, machine learning, and system design, making it a comprehensive solution for modern recommendation challenges. It not only enhances user experience but also serves as a strong demonstration of building real-world, scalable AI-driven applications.

_**ARCHITECTURE DETAILS**_
For details on the architecture and implementation, visit this codelabs documenattion.

[![Codelabs Tutorial](https://img.shields.io/badge/Codelabs_Tutorial-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://codelabs-preview.appspot.com/?file_id=1z-pGIA6HOZregKgnnslvBE-ZZRUS_rhmiQvnVc8Xoww#0)

_**PROJECT STRUCTURE**_

``` 
.github
   |-- flow
   |   |-- ci.yml
.gitignore
Dockerfile
README.md
airflow_rec
   |-- dags
   |   |-- __init__.py
   |   |-- data_extraction.py
   |-- src
   |   |-- __init__.py
   |   |-- data_cleaning.py
   |   |-- rag_implementation.py
   |   |-- similarity_search.py
   |   |-- snowflake_upload.py
   |   |-- trailer_extract.py
bingewatch.py
contentapi.py
db_module
   |-- __init__.py
   |-- db.py
   |-- user_handler.py
docker-compose.yaml
main.py
models
   |-- __init__.py
   |-- pydantic_validators.py
   |-- user_model.py
requirements.txt
unit_testing.py
utils.py
```

_**TECHNOLOGY STACK**_

[![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)](https://cloud.google.com)
[![Python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Pinecone](https://img.shields.io/badge/Pinecone-FF6F00?style=for-the-badge&logo=pinecone&logoColor=white)](https://www.pinecone.io)
[![Streamlit](https://img.shields.io/badge/streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![The Movie Database](https://img.shields.io/badge/TMDB-01D277?style=for-the-badge&logo=themoviedatabase&logoColor=white)](https://www.themoviedb.org)
[![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com)
[![Apache Airflow](https://img.shields.io/badge/Apache_Airflow-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white)](https://airflow.apache.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)

_**DATA SOURCE**_

The data source consists of records from Netflix, Hulu, Amazon Prime and DisneyPlus 

- **Kaggle**: Curated datasets from a broad range of streaming content.
- **TMDb API**: Real-time data access to movies and TV shows metadata.

_**RUN APP LOCALLY**_

1. Clone the repo.
2. Install the dependencies.
```
pip install -r requirements.txt 
```
3. Run the Dockerfile to generate the image and run the Docker compose file to bring up the instances.
```
docker build -t <image_name> .
```
```
docker compose up -d
```
This will create an airflow instance, postgresDB, streamlit for frontend and fastapi for backend.



**THANK YOU.**


**_PROJECT BY : PAARVI BHAMBRI_**
