from schemas.youtube_url import DownloadRequest
from services.download_audio import get_download_audio, DownloadAudio, cleanup_temp_file
from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException
from fastapi.responses import FileResponse
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
    try:
        filepath, title = download_youtube_audio.download_audio(url_str)
        response = FileResponse(
            path=filepath,
            media_type="audio/mpeg",
            filename=f"{title}.mp3"  # How the user sees it
        )
        background_tasks.add_task(cleanup_temp_file, filepath)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

