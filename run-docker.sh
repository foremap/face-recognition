#!/bin/bash
DOCKER_IMG="demo/32bit"
DEMO_CONTAINER_NAME="demo-service"
UPLOAD_FOLDER=$(pwd)/uploads
OMRON=$(pwd)/omron
FLASK=$(pwd)/flask-server

docker run -d \
   --name $DEMO_CONTAINER_NAME \
   -v $OMRON:/opt/omron \
   -v $FLASK:/opt/flask-server \
   -v $UPLOAD_FOLDER:/opt/uploads \
   -p 8888:8888 \
   $DOCKER_IMG
