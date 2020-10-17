# densepose_wrapper
[DensePose](https://github.com/facebookresearch/DensePose) の推論スクリプト `tools/infer_simple.py` のラッパーモジュール。<br>
以下の機能を追加しています。

- docker 環境に対応。（公式の dockerfile やインストール方法では動作しなかったため）
- サーバー機能を追加。
- 追加予定
    - UV 値の等高線表示画像の出力
    - keypoints も取得可能

## ■ 動作環境

- docker
- nvidia-docker2
- docker-compose
- nvidia 製 GPU 搭載マシン
    - K80 インスタンスでの動作を確認済み
    - T4 インスタンスでは動作しないことを確認済み
- 5003 番ポートの開放（サーバー機能使用時のデフォルト設定）

## ■ 使い方

### ◎ サーバー API 機能非使用時

`run_densepose.sh` のパラメーターを変更後、以下のコマンドを実行
```sh
$ sh run_densepose.sh
```

又は、以下のコマンドを実行

```sh
# 1. データセットの準備
$ sh fetch_densepose_data.sh

# 2. docker イメージの作成＆コンテナ起動
$ docker-compose stop
$ docker-compose up -d
$ sleep 5

# 3. densepose の推論スクリプトの実行
$ docker exec -it densepose_container /bin/bash -c \
    "python2 tools/infer_simple.py \
        --cfg configs/DensePose_ResNet101_FPN_s1x-e2e.yaml \
        --output-dir ${OUTPUT_DIR} \
        --image-ext ${FILE_EXT} \
        --wts https://dl.fbaipublicfiles.com/densepose/DensePose_ResNet101_FPN_s1x-e2e.pkl \
        ${IMAGE_FILE}"

# 4. UV 等高線の表示（実装中）
```
- `${OUTPUT_DIR}` : 出力ディレクトリ（例 : `results/sample_n5`）
- `${FILE_EXT}` : 画像ファイルの拡張子 ("jpg" or "png")
- `${IMAGE_FILE}` : 入力画像のディレクトリ（例 : `DensePoseData/infer_data/sample_n5`）
    - `DensePoseData/infer_data` 以下のディレクトリである必要があります


### ◎ サーバー API 機能使用時
サーバー機能使用時は、デフォルト設定では、`5003` 番ポートが開放されている必要があります。
使用するポート番号は、`docker-compose.yml` 内の `ports:` タグ、及び、`api/app.py`, `api/request.py` の `--port` 引数の値を設定することで変更できます。<br>

`run_densepose_request.sh` のパラメーターを変更後、以下のコマンドを実行
```sh
$ sh  run_densepose_request.sh
```

又は、以下のコマンドを実行

```sh
# 1. データセットの準備
$ sh fetch_densepose_data.sh

# 2. docker イメージの作成＆コンテナ起動
$ docker-compose stop
$ docker-compose up -d
$ sleep 5

# 3. リクエスト送信
$ cd api
$ python request.py \
    --port 5003 \
    --in_image_dir "${INPUT_DIR}" \
    --results_dir "${OUTPUT_DIR}" \
    --debug
```
- `${INPUT_DIR}` : 入力ディレクトリ（例 : `../infer_data/sample_n5`）
- `${OUTPUT_DIR}` : 出力ディレクトリ（例 : `../results_api/sample_n5`）
