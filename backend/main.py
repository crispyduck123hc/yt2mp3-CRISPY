import yt_dlp
import os
from pydantic import BaseModel, HttpUrl
from fastapi import FastAPI, BackgroundTasks
from yt_dlp import DownloadError

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "YouTube to MP3 Backend is Running!"}

# Ensure a downloads folder exists
DOWNLOAD_DIR = "../yt-downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def download_youtube_audio(url: str) -> None:
    ydl_opts = {
        'format': 'bestaudio/best',
        # This tells yt-dlp to use FFmpeg to convert the file
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        # Saves the file into our downloads folder
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except DownloadError as e:
        print(f"Failed to download: {e}")
        # In a real app, you'd update a database status here to 'FAILED'

class DownloadRequest(BaseModel):
    url: HttpUrl

@app.post("/download")
async def start_download(request: DownloadRequest, background_tasks: BackgroundTasks):
    url_str = str(request.url)
    background_tasks.add_task(download_youtube_audio, url_str)
    return {"message": "Conversion started! Check your downloads folder soon."}