docker build -t youtube-to-mp3 .
docker run -p 8000:8000 -v $(pwd)/yt-downloads:/app/yt-downloads youtube-to-mp3