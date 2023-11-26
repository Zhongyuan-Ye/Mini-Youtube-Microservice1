# Mini-Youtube-Microservice1
Mini-Youtube Microservice1: Videos Part

## Overall video storage & Distribution:
Search, fetch, upload, delete Videos. 

All the Videos side action are archieved through this microservice

upload:
'curl -X POST http://ec2-3-140-208-26.us-east-2.compute.amazonaws.com:1024/upload/ -F "file=@./video111.mp4"'

fetch:
'curl http://ec2-3-140-208-26.us-east-2.compute.amazonaws.com:1024/fetch/13452.mp4'

delete:
'curl -X DELETE http://ec2-3-140-208-26.us-east-2.compute.amazonaws.com:1024/delete/video111.mp4'
