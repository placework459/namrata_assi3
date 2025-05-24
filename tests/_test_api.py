from unittest.mock import patch
import pytest
from main import app  # Adjust this import based on where your FastAPI app is located
from fastapi.testclient import TestClient

# Mocked model
class MockModel:
    def predict(self, input_data):
        # Simulate a simple prediction
        return [500000]

# Create TestClient instance for the FastAPI app
client = TestClient(app)

# Test case for valid input using the mocked model
@patch('main.pickle.load', return_value=MockModel())  # Mock the pickle.load method
def test_predict_price_valid_input(mock_pickle):
    data = {
        "square_feet": 1500,
        "bedrooms": 3,
        "location_score": 8.0
    }
    
    response = client.post("/predict", json=data)
    
    # Assert the response status code is 200
    assert response.status_code == 200
    
    # Assert the response body contains the predicted price
    response_data = response.json()
    assert "predicted_price" in response_data
    assert isinstance(response_data["predicted_price"], (float, int))  # Ensure it is a number
