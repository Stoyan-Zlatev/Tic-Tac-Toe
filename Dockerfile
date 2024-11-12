# Dockerfile

# Use the official Python image from Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libsdl2-2.0-0 libsdl2-image-2.0-0 libsdl2-mixer-2.0-0 libsdl2-ttf-2.0-0 \
    libsdl2-gfx-1.0-0 fontconfig && \
    rm -rf /var/lib/apt/lists/*

# Copy the project files into the container
COPY . /app

# Install the Python dependencies
RUN pip install --no-cache-dir pygame

# Set the command to run the game
CMD ["python", "main.py"]
