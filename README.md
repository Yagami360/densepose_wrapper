# densepose_wrapper
[DensePose](https://github.com/facebookresearch/DensePose) の推論スクリプト `tools/infer_simple.py` のラッパーモジュール。<br>
以下の機能を追加しています。

- docker 環境に対応。（公式の dockerfile やインストール方法では動作しなかったため）
- keypoints も取得可能にする予定
- サーバー機能を追加予定。

## ■ 動作環境

- docker
- nvidia-docker2
- docker-compose
- nvidia 製 GPU 搭載マシン
    - K80 インスタンスでの動作を確認済み
    - T4 インスタンスでは動作しないことを確認済み

## ■ 使い方

### ◎ `run_densepose.sh` を利用する場合

`run_densepose.sh` のパラメーターを変更後、以下のコマンドを実行

```sh
$ sh run_densepose.sh
```

### ◎ `run_densepose.sh` を利用しない場合

1. データセットの準備
    ```sh
    $ sh sh fetch_densepose_data.sh
    ```

1. docker イメージの作成＆コンテナ起動
    ```sh
    $ docker-compose stop
    $ docker-compose up -d
    ```

1. densepose の推論スクリプトの実行
    ```sh
    $ docker exec -it densepose_container /bin/bash -c \
        "python2 tools/infer_simple.py \
            --cfg configs/DensePose_ResNet101_FPN_s1x-e2e.yaml \
            --output-dir ${OUTPUT_DIR} \
            --image-ext ${FILE_EXT} \
            --wts https://dl.fbaipublicfiles.com/densepose/DensePose_ResNet101_FPN_s1x-e2e.pkl \
            ${IMAGE_FILE}"
    ```
    - `${OUTPUT_DIR}` : 出力ディレクトリ（例 : `results/sample_n5`）
    - `${FILE_EXT}` : 画像ファイルの拡張子 ("jpg" or "png")
    - `${IMAGE_FILE}` : 入力画像のディレクトリ（例 : `DensePoseData/infer_data/sample_n5`）
        - `DensePoseData/infer_data` 以下のディレクトリである必要があります

1. UV 等高線の表示
    ```sh
    ```
