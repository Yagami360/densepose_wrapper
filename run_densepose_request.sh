#!/bin/sh
set -eu
ROOT_DIR=${PWD}
DENSEPOSE_DIR=${ROOT_DIR}/DensePose
CONTAINER_NAME=densepose_container

FILE_EXT=jpg
IMAGE_FILE=infer_data/sample_n5
OUTPUT_DIR=results/sample_n5

sudo rm -rf ${OUTPUT_DIR}
sudo mkdir -p ${OUTPUT_DIR}

# データセットの準備
sh fetch_densepose_data.sh

# コンテナ起動
cd ${ROOT_DIR}
docker-compose stop
docker-compose up -d

# densepose の実行
cd api

python request.py \
    --port 5003 \
    --in_image_dir "../${IMAGE_FILE}" \
    --results_dir "../${OUTPUT_DIR}" \
    --debug
