import os

from schemas.youtube_url import DownloadUrl
from services.download_audio import get_download_audio, DownloadAudio, cleanup_temp_file
from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException, APIRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
api_router = APIRouter(prefix="/api")

@api_router.post("/title")
async def get_title(
        request: DownloadUrl,
        download_youtube_audio: DownloadAudio = Depends(get_download_audio)
):
    url_str = str(request.url)
    return download_youtube_audio.get_title(url_str)

@api_router.post("/download")
async def start_download(
        request: DownloadUrl,
        background_tasks: BackgroundTasks,
        download_youtube_audio: DownloadAudio = Depends(get_download_audio)
):
    url_str = str(request.url)
    try:
        filepath = download_youtube_audio.download_audio(url_str)
        response = FileResponse(
            path=filepath,
            media_type="audio/mpeg",
            filename=f"audio.mp3"
        )
        background_tasks.add_task(cleanup_temp_file, filepath)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

# Include router into app after routes are defined
app.include_router(api_router)

# Get the directory of main.py: (backend)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Go up one level to the project root, then into frontend/dist
FRONTEND_DIST = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend", "dist"))

# MOUNT THE STATIC ASSETS
# Now points to project-root/frontend/dist/assets
if os.path.exists(os.path.join(FRONTEND_DIST, "assets")):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="assets")

# THE CATCH-ALL for frontend service
# TODO: does this need to be async if its just serving html?
@app.get("/{catchall:path}")
async def serve_frontend():
    index_path = os.path.join(FRONTEND_DIST, "index.html")

    if os.path.exists(index_path):
        return FileResponse(index_path)

    return {
        "error": "Frontend not built.",
        "debug_path_searched": index_path
    }