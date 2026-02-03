# 1. Use a lightweight Python base image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Install FFmpeg (and other system dependencies)
# We need 'ffmpeg' for the conversion and 'ca-certificates' for secure downloads
RUN apt-get update && apt-get install -y \
    ffmpeg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy and install Python dependencies
# Doing this before copying the rest of the code optimizes Docker's cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code
COPY . .

# 6. Create the downloads directory inside the container
RUN mkdir -p yt-downloads

# 7. Expose the port FastAPI will run on
EXPOSE 8000

# 8. Run the application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]