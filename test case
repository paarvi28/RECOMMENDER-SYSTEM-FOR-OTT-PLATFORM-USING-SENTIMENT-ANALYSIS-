import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from contentapi import fetch_movies_by_ids, app  # Ensure correct import paths

client = TestClient(app)

def test_fetch_movies_by_ids():
    # Mock data that mimics the database output
    mock_movies = [
        ("Inception", "Christopher Nolan", "Leonardo DiCaprio", 2010, 148, "Netflix", "url_to_trailer", "url_to_thumbnail", "123"),
        # Add more examples as needed
    ]

    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = mock_movies
    
    # Create a mock connection object
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor

    # Patch the snowflake.connector.connect to return the mock connection
    with patch('snowflake.connector.connect', return_value=mock_connection):
        # Adjust the call to include 'content_type'
        result = fetch_movies_by_ids('movie', ['123', '456'])  # Example unique_ids
        assert len(result) == len(mock_movies)
        assert result == mock_movies

        # Check if cursor methods are called as expected
        mock_cursor.execute.assert_called_once()
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

def test_get_movies():
    # Mock the response from fetch_movies_by_ids
    with patch("contentapi.fetch_movies_by_ids") as mock_fetch:
        mock_fetch.return_value = [
            ("Inception", "Christopher Nolan", "Leonardo DiCaprio", 2010, 148, "Netflix", "url_to_trailer", "url_to_thumbnail", "123"),
            # Add more examples as needed
        ]
        # Adjust the API call to match the new endpoint and parameters
        response = client.get("/content?content_type=movie&unique_ids=123,456")
        assert response.status_code == 200
        assert response.json() == [
            {
                "title": "Inception",
                "director": "Christopher Nolan",
                "cast_member": "Leonardo DiCaprio",
                "release_year": 2010,
                "duration": 148,
                "available_on": "Netflix",
                "trailer": "url_to_trailer",
                "thumbnail": "url_to_thumbnail",
                "unique_id": "123"
            }
        ]

        # Test the case where no movies are found
        mock_fetch.return_value = []
        response = client.get("/content?content_type=movie&unique_ids=999")
        assert response.status_code == 200
        assert response.json() == {"error": "No movies found"}
