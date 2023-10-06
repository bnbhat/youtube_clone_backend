from pydantic import BaseModel
from datetime import datetime

class VideoMataData(BaseModel):
    title: str
    description: str
    upload_date: datetime
    file_path: str
