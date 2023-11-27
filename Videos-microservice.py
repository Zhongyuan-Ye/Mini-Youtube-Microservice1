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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1024)
