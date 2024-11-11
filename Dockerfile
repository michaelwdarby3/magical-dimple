# Base image
FROM python:3.9

# Set the working directory
WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client

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
# Copy the start.sh script into the Docker image
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Use the script as the default command
CMD ["/start.sh"]