from fastapi import FastAPI
from app.api.v1.users import endpoints as user_endpoints
from app.api.v1.videos import endpoints as video_endpoints

app = FastAPI()

app.include_router(user_endpoints.router, prefix="/api/v1/users")
app.include_router(video_endpoints.router, prefix="/api/v1/videos")

