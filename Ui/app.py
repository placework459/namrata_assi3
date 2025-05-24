import os
import gradio as gr
import pickle

# Get the absolute path to the model
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'model', 'model.pkl')

# Check if the model file exists
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file '{model_path}' not found!")

# Load trained model
model = pickle.load(open(model_path, "rb"))

# Define the prediction function
def predict_price(square_feet, bedrooms, location_score):
    input_data = [[square_feet, bedrooms, location_score]]
    prediction = model.predict(input_data)[0]
    return prediction

# Create the Gradio interface
demo = gr.Interface(
    fn=predict_price,
    inputs=[
        gr.Number(label="Square Feet"),
        gr.Number(label="Bedrooms"),
        gr.Number(label="Location Score")
    ],
    outputs=gr.Number(label="Predicted Price"),
    title="House Price Predictor"
)

if __name__ == "__main__":
    demo.launch(share=True)
