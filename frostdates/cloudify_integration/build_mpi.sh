#!/bin/bash

export IMAGE_NAME=agroclimatic_zone_frostdates
export IMAGE_TAG=mpi
export REGISTRY_ADRESS=registry.test.euxdat.eu/euxdat

docker build --rm=true -t $IMAGE_NAME . 
docker tag $IMAGE_NAME $REGISTRY_ADRESS/$IMAGE_NAME:$IMAGE_TAG 
docker push  $REGISTRY_ADRESS/$IMAGE_NAME:$IMAGE_TAG

