# Mini-Youtube-Microservice1
Mini-Youtube Microservice1: Videos Part

## Overall video storage & Distribution:
Search, fetch, upload, delete Videos. 

All the Videos side action are archieved through this microservice

upload:
curl -X POST -F "file=@C:\Users\zhong\Downloads\video-example\micro3.mp4" http://ec2-3-140-208-26.us-east-2.compute.amazonaws.com:1024/upload-video/

fetch: 
'http://ec2-3-140-208-26.us-east-2.compute.amazonaws.com:1024/fetch-video/micro3.mp4'

delete:
'curl -X DELETE http://ec2-3-140-208-26.us-east-2.compute.amazonaws.com:1024/delete-video/micro3.mp4'
