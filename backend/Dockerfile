# Use the lightweight Debian-based Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /backend

# Copy the application code into the container
COPY . .

# Install system dependencies required for psycopg2-binary and Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# Expose the port your app runs on
EXPOSE 5003

# Define the entry point for the container
ENTRYPOINT ["python", "app.py"]