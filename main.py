from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import os
import threading
import gradio as gr
from Ui.app import predict_price  # Assuming the function in Ui/app.py is named predict_price

# Define FastAPI app
app = FastAPI(title="House Price Prediction API")

# Model loading with error handling
model_path = os.path.join("model", "model.pkl")
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file '{model_path}' not found!")

with open(model_path, "rb") as f:
    model = pickle.load(f)

# Define request format (input data schema)
class InputData(BaseModel):
    square_feet: float
    bedrooms: int
    location_score: float

# Define prediction endpoint
@app.post("/predict")
def predict_price_endpoint(data: InputData):
    # Prepare input data for prediction
    input_data = [[data.square_feet, data.bedrooms, data.location_score]]
    
    # Make prediction using the model
    try:
        prediction = model.predict(input_data)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
    
    # Return the predicted price
    return {"predicted_price": prediction}

# Function to start Gradio UI in a separate thread
def start_gradio():
    iface = gr.Interface(
        fn=predict_price,
        inputs=[gr.Number(label="Square Feet"), gr.Number(label="Bedrooms"), gr.Number(label="Location Score")],
        outputs=gr.Number(label="Predicted Price"),
        title="House Price Predictor",
        live=True  # Enables live updates when inputs are changed
    )
    # Explicitly set server_name and server_port for proper async handling
    iface.launch(share=True, inbrowser=True, server_name="127.0.0.1", server_port=7862)

# Start Gradio UI in a background thread
def run_gradio_in_background():
    thread = threading.Thread(target=start_gradio)
    thread.daemon = True  # This allows the thread to exit when the main program exits
    thread.start()

# Run Gradio UI on startup
@app.on_event("startup")
async def startup_event():
    run_gradio_in_background()
