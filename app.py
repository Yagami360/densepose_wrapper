# coding=utf-8
import os
import sys
import argparse
import json
from PIL import Image
import cv2
import numpy as np
import itertools

# flask
import flask
from flask_cors import CORS

# DensePose
sys.path.append(os.path.join(os.getcwd(), 'DensePose/tools'))
from inference import inference

# 自作モジュール
from utils import conv_base64_to_pillow, conv_pillow_to_base64

#======================
# グローバル変数
#======================
#-------------------
# flask 関連
#-------------------
app = flask.Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}}, methods=['POST', 'GET'])  # OPTIONS を受け取らないようにする（Access-Control-Allow-Origin エラー対策）
app.config['JSON_AS_ASCII'] = False     # 日本語文字化け対策
app.config["JSON_SORT_KEYS"] = False    # ソートをそのまま

#-------------------
# densepose 関連
#-------------------
args = False

#================================================================
# "http://host_ip:port_id" リクエスト送信時の処理
#================================================================
@app.route('/')
def index():
    print "リクエスト受け取り"
    return

#================================================================
# "http://host_ip:port_id/densepose" にリクエスト送信時の処理
#================================================================
@app.route('/densepose', methods=['POST'])
def responce():
    print "リクエスト受け取り"
    if( app.debug ):
        print "flask.request.method : ", flask.request.method
        print "flask.request.headers \n: ", flask.request.headers

    #------------------------------------------
    # 送信された json データの取得
    #------------------------------------------
    if( flask.request.headers["User-Agent"].split("/")[0] in "python-requests" ):
        json_data = json.loads(flask.request.json)
    else:
        json_data = flask.request.get_json()

    #------------------------------------------
    # 送信された画像データの変換
    #------------------------------------------
    pose_img_pillow = conv_base64_to_pillow( json_data["pose_img_base64"] )
    pose_img_pillow.save( os.path.join( "tmp", "pose_img.png" ) )

    #------------------------------------------
    # DensePose の実行
    #------------------------------------------
    in_img_path = os.path.join( "tmp", "pose_img.png" )
    pose_parse_img_np = inference( args )
    pose_parse_img_pillow = Image.fromarray( np.uint8(pose_parse_img_np.transpose(0,1)) , 'L')
    pose_parse_img_pillow.save( os.path.join( "tmp", "pose_parse_img.png" ) )

    #------------------------------------------
    # 送信する画像データの変換
    #------------------------------------------
    pose_parse_img_base64 = conv_pillow_to_base64( pose_parse_img_pillow )

    #------------------------------------------
    # レスポンスメッセージの設定
    #------------------------------------------
    http_status_code = 200
    response = flask.jsonify(
        {
            'status':'OK',
            'pose_parse_img_base64': pose_parse_img_base64,
        }
    )

    # レスポンスメッセージにヘッダーを付与（Access-Control-Allow-Origin エラー対策）
    #response.headers.add('Access-Control-Allow-Origin', '*')
    #response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    #response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    if( app.debug ):
        print "response.headers : \n", response.headers

    return response, http_status_code


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #parser.add_argument('--host', type=str, default="localhost", help="ホスト名（コンテナ名 or コンテナ ID）")
    parser.add_argument('--host', type=str, default="0.0.0.0", help="ホスト名（コンテナ名 or コンテナ ID）")
    parser.add_argument('--port', type=str, default="5003", help="ポート番号")
    parser.add_argument('--enable_threaded', action='store_true', help="並列処理有効化")
    parser.add_argument('--debug', action='store_true', help="デバッグモード有効化")
    parser.add_argument('--cfg', dest='cfg', help='cfg model file (/path/to/model_config.yaml)', default="DensePose/configs/DensePose_ResNet101_FPN_s1x-e2e.yaml", type=str)
    parser.add_argument('--wts', dest='weights', help='weights model file (/path/to/model_weights.pkl)', default="https://dl.fbaipublicfiles.com/densepose/DensePose_ResNet101_FPN_s1x-e2e.pkl", type=str)
    parser.add_argument('--output-dir', dest='output_dir', help='directory for visualization pdfs (default: /tmp/infer_simple)', default='results', type=str)
    parser.add_argument('--image-ext', dest='image_ext', help='image file name extension (default: jpg)', default='jpg', type=str)
    parser.add_argument('im_or_folder', help='image or folder of images', default="sample_n5")
    args = parser.parse_args()
    if( args.debug ):
        for key, value in vars(args).items():
            print '%s: %s' % (str(key), str(value))

    if not os.path.exists("tmp"):
        os.mkdir("tmp")
        
    # グローバル変数に引数を反映
    args = args

    #--------------------------
    # Flask の起動
    #--------------------------
    app.debug = args.debug
    if( args.enable_threaded ):
        app.run( host=args.host, port=args.port, threaded=False )
    else:
        app.run( host=args.host, port=args.port, threaded=True )