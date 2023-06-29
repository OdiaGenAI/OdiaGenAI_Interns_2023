# Use the official Python base image
FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Expose the port on which your Streamlit app will run
EXPOSE 8501

# Run the Streamlit app when the container starts
CMD ["streamlit", "run", "app.py"]
