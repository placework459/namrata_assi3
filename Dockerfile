# Use a specific Python version (slim version to keep the image smaller)
FROM python:3.11-slim

# Set the working directory in the container (where the app will be located)
WORKDIR /App

# Copy the requirements.txt into the container at the working directory
COPY requirements.txt .

# Install Python dependencies from the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the application will run on (7860 for Gradio by default)
EXPOSE 7860

# Command to run the app (make sure to adjust if you have a different entry point)
CMD ["python", "main.py"]

