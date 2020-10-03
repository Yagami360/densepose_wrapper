#!/bin/sh
set -eu
ROOT_DIR=${PWD}
DENSEPOSE_DIR=${ROOT_DIR}/DensePose
CONTAINER_NAME=densepose_container

FILE_EXT=jpg
IMAGE_FILE=DensePoseData/demo_data/demo_im.jpg
OUTPUT_DIR=DensePoseData/infer_out
#OUTPUT_DIR=results

# データセットの準備
cd ${DENSEPOSE_DIR}/DensePoseData
if [ ! -e ${DENSEPOSE_DIR}/DensePoseData/DensePose_COCO ] ; then
    bash get_DensePose_COCO.sh
fi
if [ ! -e ${DENSEPOSE_DIR}/DensePoseData/UV_data ] ; then
    bash get_densepose_uv.sh
fi
if [ ! -e ${DENSEPOSE_DIR}/DensePoseData/eval_data ] ; then
    bash get_eval_data.sh
fi

# コンテナ起動
cd ${ROOT_DIR}
docker-compose stop
docker-compose up -d

#<<COMMENTOUT
docker exec -it ${CONTAINER_NAME} /bin/bash -c \
    "python2 tools/infer_simple.py \
        --cfg configs/DensePose_ResNet101_FPN_s1x-e2e.yaml \
        --output-dir ${OUTPUT_DIR} \
        --image-ext ${FILE_EXT} \
        --wts https://dl.fbaipublicfiles.com/densepose/DensePose_ResNet101_FPN_s1x-e2e.pkl \
        ${IMAGE_FILE}"
#COMMENTOUT

#docker exec -it ${CONTAINER_NAME} /bin/bash