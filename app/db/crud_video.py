from app.models.video_matadata import VideoMataData
from app.db.mongodb import database

video_collection = database.get_collection("videos")

async def create_video(video: VideoMataData):
    video_data = video.dict()
    await video_collection.insert_one(video_data)
