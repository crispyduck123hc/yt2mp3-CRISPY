# note: this is a development dockerfile, the volume mounting in compose overrides the copy.
# Use a lightweight Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install FFmpeg (and other system dependencies)
# We need 'ffmpeg' for the conversion and 'ca-certificates' for secure downloads
RUN apt-get update && apt-get install -y \
    ffmpeg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies as separate layer for efficiency.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# server binding to 0.0.0.0, provide access to all network interfaces.
# use port 8000
# "main:app" to search for main module I needed to set the pythonpath env var so that interpreter can find it
# dev environment
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]