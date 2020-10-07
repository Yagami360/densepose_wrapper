#!/bin/sh
#nohup sh run_densepose.sh > run_densepose_201005.out &
#nohup sh run_densepose.sh poweroff > run_densepose_201005.out &
#set -eu
ROOT_DIR=${PWD}
DENSEPOSE_DIR=${ROOT_DIR}/DensePose
CONTAINER_NAME=densepose_container

#FILE_EXT=jpg
#IMAGE_FILE=DensePoseData/demo_data/demo_im.jpg
#IMAGE_FILE=DensePoseData/infer_data/sample_n5

#--------------------------------
# pose A
#--------------------------------
FILE_EXT=png
IMAGE_FILE=DensePoseData/infer_data/outfit_dataset_male_female_wo_back_wo_elbow_256_revise3/poseA
OUTPUT_DIR=results/outfit_dataset_male_female_wo_back_wo_elbow_256_revise3/poseA_densepose
sudo mkdir -p results
sudo mkdir -p results/outfit_dataset_male_female_wo_back_wo_elbow_256_revise3
sudo mkdir -p ${OUTPUT_DIR}
sudo rm -rf ${OUTPUT_DIR}

# コンテナ起動
cd ${ROOT_DIR}
docker-compose stop
docker-compose up -d

# densepose の実行
docker exec ${CONTAINER_NAME} /bin/bash -c \
    "python2 tools/infer_simple.py \
        --cfg configs/DensePose_ResNet101_FPN_s1x-e2e.yaml \
        --output-dir ${OUTPUT_DIR} \
        --image-ext ${FILE_EXT} \
        --wts https://dl.fbaipublicfiles.com/densepose/DensePose_ResNet101_FPN_s1x-e2e.pkl \
        ${IMAGE_FILE}"

#docker exec -it ${CONTAINER_NAME} /bin/bash

#--------------------------------
# pose B
#--------------------------------
FILE_EXT=png
IMAGE_FILE=DensePoseData/infer_data/outfit_dataset_male_female_wo_back_wo_elbow_256_revise3/poseB
OUTPUT_DIR=results/outfit_dataset_male_female_wo_back_wo_elbow_256_revise3/poseB_densepose
sudo mkdir -p results
sudo mkdir -p results/outfit_dataset_male_female_wo_back_wo_elbow_256_revise3
sudo mkdir -p ${OUTPUT_DIR}
sudo rm -rf ${OUTPUT_DIR}

# コンテナ起動
cd ${ROOT_DIR}
docker-compose stop
docker-compose up -d

# densepose の実行
docker exec ${CONTAINER_NAME} /bin/bash -c \
    "python2 tools/infer_simple.py \
        --cfg configs/DensePose_ResNet101_FPN_s1x-e2e.yaml \
        --output-dir ${OUTPUT_DIR} \
        --image-ext ${FILE_EXT} \
        --wts https://dl.fbaipublicfiles.com/densepose/DensePose_ResNet101_FPN_s1x-e2e.pkl \
        ${IMAGE_FILE}"


if [ $1 = "poweroff" ] ; then
    sudo poweroff
    sudo shutdown -h now
fi
