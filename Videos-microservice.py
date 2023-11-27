from fastapi import FastAPI, UploadFile, File, HTTPException
import boto3
from botocore.exceptions import NoCredentialsError
import uvicorn

app = FastAPI()

# Initialize S3 client
s3_client = boto3.client('s3')
bucket_name = 'storage-microservice'

@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    try:
        s3_client.upload_fileobj(file.file, bucket_name, file.filename)
        return {"message": f"'{file.filename}' uploaded successfully"}
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="Credentials not available")

from fastapi.responses import StreamingResponse



@app.get("/fetch-video/{username}/{video_id}")
async def fetch_video(username: str, video_id: str):
    query = "SELECT * FROM videos WHERE video_id = :video_id"
    video = await database.fetch_one(query=query, values={"video_id": video_id})
    if video and (video['uploader'] == username or video['publicity']):
        response = requests.get(f"{ms1_url}/fetch-video/{video_id}.mp4", stream=True)
        if response.status_code == 200:
            return StreamingResponse(response.iter_content(chunk_size=1024*1024), media_type="video/mp4")
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching video")
    else:
        raise HTTPException(status_code=404, detail="Video not found or access denied")



@app.delete("/delete-video/{file_name}")
async def delete_video(file_name: str):
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=file_name)
        return {"message": f"'{file_name}' deleted successfully"}
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="Credentials not available")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1024)
