import pickle
import pytest
import gradio as gr
from unittest import mock

# Mocking the model loading process for CI/CD
def mock_model_predict(input_data):
    return [500000.0]  # Example predicted price

def predict_price(square_feet, bedrooms, location_score):
    # Validate inputs
    if not isinstance(square_feet, (int, float)) or not isinstance(bedrooms, int) or not isinstance(location_score, (int, float)):
        raise ValueError("Invalid input types. Expected numbers for square_feet, bedrooms, and location_score.")
    
    # For testing, we mock the model loading
    model = mock_model_predict
    input_data = [[square_feet, bedrooms, location_score]]
    prediction = model(input_data)[0]
    return prediction

# Test: Valid input for prediction
def test_predict_price_valid_input():
    result = predict_price(1200, 3, 7.5)
    assert isinstance(result, (float, int)), "Output should be a number"
    assert result > 0, "Predicted price should be positive"

# Test: Gradio interface
def test_gradio_interface():
    demo = gr.Interface(
        fn=predict_price,
        inputs=[gr.Number(label="Square Feet"), gr.Number(label="Bedrooms"), gr.Number(label="Location Score")],
        outputs=gr.Number(label="Predicted Price"),
    )
    result = demo.fn(1000, 2, 6.0)
    assert isinstance(result, (float, int)), "Output should be a number"
    assert result > 0, "Predicted price should be positive"

# Test: Invalid input
def test_invalid_input():
    with pytest.raises(ValueError):  
        predict_price("invalid_input", 2, 6.0)

# Test: Gradio interface with invalid input
def test_gradio_invalid_input():
    demo = gr.Interface(
        fn=predict_price,
        inputs=[gr.Textbox(label="Square Feet"), gr.Number(label="Bedrooms"), gr.Number(label="Location Score")],
        outputs=gr.Number(label="Predicted Price"),
    )
    try:
        result = demo.fn("invalid_input", 2, 6.0)
    except ValueError as e:
        result = str(e)  # Capture the error message
    
    assert isinstance(result, str), "Expected an error message or warning"
    assert "Invalid input types" in result, "Result should contain an error message for invalid input"
