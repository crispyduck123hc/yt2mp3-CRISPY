import uuid
import yt_dlp
import os

class DownloadAudio:
    def __init__(self, download_dir: str = "./tmp"):
        self.download_dir = download_dir
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def download_audio(self, url: str) -> tuple[str, str]:
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'audio_download')
        unique_filename = str(uuid.uuid4())
        filepath = f"{self.download_dir}/{unique_filename}.mp3"
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': f"{self.download_dir}/{unique_filename}.%(ext)s",
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return filepath, video_title

_download_service = DownloadAudio()

def get_download_audio() -> DownloadAudio:
    return _download_service

def cleanup_temp_file(path: str):
    """Helper function to delete the file after streaming"""
    if os.path.exists(path):
        os.remove(path)