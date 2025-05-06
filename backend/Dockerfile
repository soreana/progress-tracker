# Use official Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements (if any)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY app.py .

# Expose Flask default port
EXPOSE 5000

# Set the environment variable to tell Flask to run the app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production
ENV PAPERCLIP_TOKEN=1f2d4e7bfae448ba8c7df5c8f49b0c43b61863fd59b287b2e2de9d43115e3941

# Run the Flask app
CMD ["flask", "run"]

