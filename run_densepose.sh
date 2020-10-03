#!/bin/sh
set -eu
ROOT_DIR=${PWD}
DENSEPOSE_DIR=${ROOT_DIR}/DensePose
CONTAINER_NAME=densepose_container

FILE_EXT=jpg
IMAGE_FILE=DensePoseData/demo_data/demo_im.jpg

# コンテナ起動
cd ${ROOT_DIR}
docker-compose stop
docker-compose up -d

#<<COMMENTOUT
docker exec -it ${CONTAINER_NAME} /bin/bash -c \
    "python2 tools/infer_simple.py \
        --cfg configs/DensePose_ResNet101_FPN_s1x-e2e.yaml \
        --output-dir DensePoseData/infer_out/ \
        --image-ext ${FILE_EXT} \
        --wts https://dl.fbaipublicfiles.com/densepose/DensePose_ResNet101_FPN_s1x-e2e.pkl \
        ${IMAGE_FILE}"
#COMMENTOUT

#docker exec -it ${CONTAINER_NAME} /bin/bash