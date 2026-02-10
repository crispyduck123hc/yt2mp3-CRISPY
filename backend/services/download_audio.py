import yt_dlp
import os
from yt_dlp.utils import DownloadError

class DownloadAudio:
    def __init__(self, download_dir: str = "./yt-downloads"):
        self.download_dir = download_dir
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def download_audio(self, url: str) -> bool:
        relative_path = f'{self.download_dir}/%(title)s.%(ext)s'
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': relative_path,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return True
        except DownloadError as e:
            print(f"Service Error: {e}")
            return False

_download_service = DownloadAudio()

def get_download_audio() -> DownloadAudio:
    return _download_service