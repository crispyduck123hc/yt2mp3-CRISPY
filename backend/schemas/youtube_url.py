from pydantic import BaseModel, HttpUrl
# DTO
class DownloadRequest(BaseModel):
    url: HttpUrl