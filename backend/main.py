from schemas.youtube_url import DownloadRequest
from services.download_audio import get_download_audio
from services.download_audio import DownloadAudio
from fastapi import FastAPI, BackgroundTasks, Depends

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "YouTube to MP3 Backend is Running possibly!"}

@app.post("/download")
async def start_download(
        request: DownloadRequest,
        background_tasks: BackgroundTasks,
        download_youtube_audio: DownloadAudio = Depends(get_download_audio)
):
    url_str = str(request.url)
    background_tasks.add_task(download_youtube_audio.download_audio, url_str)
    return {"message": "Conversion started! Check your downloads folder soon."}