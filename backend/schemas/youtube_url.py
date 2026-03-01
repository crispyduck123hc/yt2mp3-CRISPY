from pydantic import BaseModel, HttpUrl
# DTO
# extra url parsing
class DownloadUrl(BaseModel):
    url: HttpUrl