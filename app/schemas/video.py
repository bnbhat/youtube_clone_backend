from pydantic import BaseModel

class VideoUpload(BaseModel):
    title: str
    description: str
