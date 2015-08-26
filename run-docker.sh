#!/bin/bash
DOCKER_IMG="demo/32bit"
DEMO_CONTAINER_NAME="demo-service"
UPLOAD_FOLDER=$(pwd)/uploads

docker run -d \
   --name $DEMO_CONTAINER_NAME \
   -v $UPLOAD_FOLDER:/opt/flask-server/uploads \
   -p 8888:8888 \
   $DOCKER_IMG