import pickle
import pytest
import gradio as gr

# Absolute path to the model
model = pickle.load(open("D:/Users/i60385/Desktop/Work/Assig_3/model/model.pkl", "rb"))



# Prediction function (should match your actual function)
def predict_price(square_feet, bedrooms, location_score):
    input_data = [[square_feet, bedrooms, location_score]]
    prediction = model.predict(input_data)[0]
    return prediction

# Sample test
def test_predict_price_valid_input():
    # Valid input for prediction
    result = predict_price(1200, 3, 7.5)
    
    # Assert that the result is a number
    assert isinstance(result, (float, int)), "Output should be a number"
    
    # Assert that the predicted price is positive
    assert result > 0, "Predicted price should be positive"

# Test for the Gradio interface
def test_gradio_interface():
    # Initialize Gradio interface
    demo = gr.Interface(
        fn=predict_price,
        inputs=[
            gr.Number(label="Square Feet"),
            gr.Number(label="Bedrooms"),
            gr.Number(label="Location Score")
        ],
        outputs=gr.Number(label="Predicted Price"),
    )
    
    # Call the function directly with test inputs and check the result
    result = demo.fn(1000, 2, 6.0)
    
    # Assert that the result is a number
    assert isinstance(result, (float, int)), "Output should be a number"
    
    # Check that the result is positive (if that's the expected behavior)
    assert result > 0, "Predicted price should be positive"

# Optionally, you can add more tests for invalid inputs, empty inputs, etc.
def test_invalid_input():
    # Invalid input: square_feet as a string instead of a number
    with pytest.raises(ValueError):  # Assuming ValueError is raised for invalid input
        predict_price("invalid_input", 2, 6.0)

def test_gradio_invalid_input():
    # Test Gradio interface with invalid input (e.g., string instead of a number)
    demo = gr.Interface(
        fn=predict_price,
        inputs=[
            gr.Textbox(label="Square Feet"),  # Deliberate wrong input type for testing
            gr.Number(label="Bedrooms"),
            gr.Number(label="Location Score")
        ],
        outputs=gr.Number(label="Predicted Price"),
    )
    
    # Test Gradio with a string for square_feet (should raise an error or be handled)
    result = demo.fn("invalid_input", 2, 6.0)
    
    # Here, you should handle the error (depending on how Gradio reacts to bad inputs)
    assert isinstance(result, str), "Expected an error message or warning"
    assert "Error" in result, "Result should contain an error message for invalid input"
