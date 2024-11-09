# Base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir protobuf==3.20.3
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY src/ /app/src
COPY dashboard/ /app/dashboard
#COPY config/ /app/config
COPY data/ /app/data
COPY monitoring/ /app/monitoring

#COPY . .

# Expose the API port (change if necessary)
EXPOSE 8000

# Command to run the application
#CMD ["python", "-m", "src.query.query_service"]

# Run the application (assuming FastAPI for example)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
