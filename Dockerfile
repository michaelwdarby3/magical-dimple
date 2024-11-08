# Base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY src/ /app/src
COPY config/ /app/config
COPY data/ /app/data

# Expose the API port (change if necessary)
EXPOSE 8000

# Command to run the application
CMD ["python", "-m", "src.query.query_service"]
