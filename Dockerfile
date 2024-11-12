# Base image
FROM python:3.9

# Set the working directory
WORKDIR /app

ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y postgresql-client

# Copy requirements and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir protobuf==3.20.3
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY src/ /app/src
COPY dashboard/ /app/dashboard
COPY data/ /app/data
COPY monitoring/ /app/monitoring

# Expose the API port
EXPOSE 8000

# Use CMD for the main app service in this Dockerfile
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
