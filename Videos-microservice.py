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

@app.get("/fetch-video/{file_name}")
async def fetch_video(file_name: str):
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        return StreamingResponse(response['Body'], media_type="video/mp4")
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="Credentials not available")
    except s3_client.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="File not found")

@app.delete("/delete-video/{file_name}")
async def delete_video(file_name: str):
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=file_name)
        return {"message": f"'{file_name}' deleted successfully"}
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="Credentials not available")




@app.get("/get-video-image/{file_name}")
async def get_video_image(file_name: str):
    try:
        # Check if video exists in S3
        s3_client.head_object(Bucket=bucket_name, Key=file_name)

        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
            # Download the video file from S3
            s3_client.download_fileobj(bucket_name, file_name, temp_file)

            # Extract an image from the video
            clip = VideoFileClip(temp_file.name)
            frame = clip.get_frame(1)  # Get a frame at 1 second

            # Save the frame as an image
            image_path = temp_file.name + ".jpg"
            clip.save_frame(image_path, 1)  # Save the frame at 1 second

            # Encode the image in base64
            with open(image_path, "rb") as image_file:
                base64_string = base64.b64encode(image_file.read()).decode()

            return JSONResponse(content={"image": base64_string})

    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="Credentials not available")
    except s3_client.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="Video not found")
    finally:
        # Clean up: remove temporary files
        if os.path.exists(temp_file.name):
            os.remove(temp_file.name)
        if os.path.exists(image_path):
            os.remove(image_path)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1024)
