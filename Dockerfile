# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install the necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire content of the root folder into the container
COPY . .

# Set the environment variables (optional)
ENV FLASK_APP=web_flask/app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Set PYTHONPATH to include the app directory
ENV PYTHONPATH=/app

# Expose the port that the app runs on
EXPOSE 5000

# Command to run the application
CMD ["flask", "run"]
