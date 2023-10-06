from fastapi import APIRouter, UploadFile, HTTPException, Header,  Form, File
from app.models.video_matadata import VideoMataData
from app.schemas.video import VideoUpload
from app.db.crud_video import create_video
import os
from app.core.config import ROOT_DIR
from datetime import datetime
from fastapi import Response
from fastapi.responses import StreamingResponse
import aiofiles

router = APIRouter()

VIDEO_DIR = os.path.join(ROOT_DIR, "uploads", "videos")

@router.post("/upload/")
async def upload_video(title: str = Form(...), description: str = Form(...), file: UploadFile = File(...)):
    print(title)
    if file:
        # Ensure the file is in the correct format (e.g., .mp4)
        if not file.filename.endswith(".mp4"):
            raise HTTPException(status_code=400, detail="Invalid file type. Only .mp4 allowed.")
        
        file_path = os.path.join(VIDEO_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        video_metadata = VideoMataData(
            title=title,
            description=description,
            upload_date=datetime.now(),
            file_path=file_path
        )
        
        await create_video(video_metadata)

        return {"message": "Video uploaded successfully", "file_path": file_path}
    
    raise HTTPException(status_code=400, detail="File not provided.")

CHUNK_SIZE = 1024*1024
#@router.get("/stream/{video_name}/")
async def stream_video(video_name: str):
    video_path = os.path.join(VIDEO_DIR, video_name + '.mp4')
    print(video_path)
    
    if not os.path.isfile(video_path):
        raise HTTPException(status_code=404, detail="Video not found")

    async def read_file(file_name: str):
        async with aiofiles.open(file_name, mode="rb") as file:
            while True:
                data = await file.read(100_000)  # read 100k bytes (customize this value as needed)
                if not data:
                    break
                yield data

    return StreamingResponse(read_file(video_path), media_type="video/mp4")


@router.get("/stream/{video_name}/")
async def stream_video(video_name: str, range: str = Header(default=None)):
    video_path = os.path.join(VIDEO_DIR, f"{video_name}.mp4")
    
    if not os.path.isfile(video_path):
        raise HTTPException(status_code=404, detail="Video not found")

    file_size = os.path.getsize(video_path)
    
    start, end = 0, file_size - 1
    
    if range:
        byte_pos = range.replace("bytes=", "").split("-")
        if byte_pos[0]:
            start = int(byte_pos[0])
        if len(byte_pos) > 1 and byte_pos[1]:
            end = int(byte_pos[1])
            
        content_length = end - start + 1

        headers = {
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Content-Length": str(content_length),
            "Accept-Ranges": "bytes",
        }

        async def read_file_range(file_name: str, start: int, end: int):
            async with aiofiles.open(file_name, mode="rb") as file:
                await file.seek(start)
                bytes_remaining = end - start + 1
                while bytes_remaining:
                    chunk_size = min(bytes_remaining, 100_000)
                    data = await file.read(chunk_size)
                    if not data:
                        break
                    bytes_remaining -= len(data)
                    yield data

        return StreamingResponse(read_file_range(video_path, start, end), status_code=206, media_type="video/mp4", headers=headers)

    else:
        return StreamingResponse(open(video_path, mode="rb"), media_type="video/mp4")

#async def stream_video2(video_name: str):
#    video_path = os.path.join(VIDEO_DIR, video_name+".mp4")
#    start, end = range.replace("bytes=", "").split("-")
#    start = int(start)
#    end = int(end) if end else start + CHUNK_SIZE
#    with open(video_path, "rb") as video:
#        video.seek(start)
#        data = video.read(end - start)
#        filesize = str(video_path.stat().st_size)
#        headers = {
#            'Content-Range': f'bytes {str(start)}-{str(end)}/{filesize}',
#            'Accept-Ranges': 'bytes'
#        }
#        return Response(data, status_code=206, headers=headers, media_type="video/mp4")
