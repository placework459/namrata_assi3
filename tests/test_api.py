from fastapi.testclient import TestClient
from main import app  # Adjust this import based on where your FastAPI app is located
import pytest

# Create TestClient instance for the FastAPI app
client = TestClient(app)

# Test case for valid input
def test_predict_price_valid_input():
    # Valid input data
    data = {
        "square_feet": 1500,
        "bedrooms": 3,
        "location_score": 8.0
    }
    
    # Send a POST request to the /predict endpoint
    response = client.post("/predict", json=data)
    
    # Assert the response status code is 200
    assert response.status_code == 200
    
    # Assert that the response body contains the predicted price
    response_data = response.json()
    assert "predicted_price" in response_data
    assert isinstance(response_data["predicted_price"], (float, int))  # Ensure it is a number

# Test case for missing fields
def test_predict_price_missing_field():
    # Missing "location_score"
    data = {
        "square_feet": 1200,
        "bedrooms": 2
    }
    
    response = client.post("/predict", json=data)
    
    # Assert the response status code is 422 (Unprocessable Entity)
    assert response.status_code == 422
    
    # Check that the error response contains an appropriate message
    response_data = response.json()
    assert "detail" in response_data
    assert isinstance(response_data["detail"], list)  # Ensure detail is a list of errors
    assert "location_score" in str(response_data["detail"][0])  # Ensure the error refers to missing location_score

# Test case for invalid input type
def test_predict_price_invalid_type():
    # Invalid type for "square_feet" (should be a float)
    data = {
        "square_feet": "invalid_value",  # String instead of float
        "bedrooms": 3,
        "location_score": 7.5
    }
    
    response = client.post("/predict", json=data)
    
    # Assert the response status code is 422 (Unprocessable Entity)
    assert response.status_code == 422
    
    # Check that the error response contains an appropriate message
    response_data = response.json()
    assert "detail" in response_data
    assert isinstance(response_data["detail"], list)  # Ensure detail is a list of errors
    assert "square_feet" in str(response_data["detail"][0])  # Ensure the error refers to invalid square_feet

# Test case for empty input (all fields missing)
def test_predict_price_empty_input():
    data = {}
    
    response = client.post("/predict", json=data)
    
    # Assert the response status code is 422 (Unprocessable Entity)
    assert response.status_code == 422
    
    # Check that the error response contains the missing fields
    response_data = response.json()
    assert "detail" in response_data
    assert len(response_data["detail"]) == 3  # We expect three missing fields: square_feet, bedrooms, location_score
    assert "square_feet" in str(response_data["detail"][0])
    assert "bedrooms" in str(response_data["detail"][1])
    assert "location_score" in str(response_data["detail"][2])

