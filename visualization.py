import os
import argparse
import numpy
import cv2
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--in_image_IUV", default="results/sample_n5/000001_0_IUV.png")
    parser.add_argument("--results_dir", default="results2")
    parser.add_argument('--image_height', type=int, default=256, help="入力画像の高さ（pixel単位）")
    parser.add_argument('--image_width', type=int, default=192, help="入力画像の幅（pixel単位）")
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    if( args.debug ):
        for key, value in vars(args).items():
            print('%s: %s' % (str(key), str(value)))

    if not os.path.isdir(args.results_dir):
        os.mkdir(args.results_dir)

    img_IUV = cv2.imread( args.in_image_IUV )

    # UV 値の等高線を plot
    fig = plt.figure(figsize=[args.image_width/100,args.image_height/100])
    plt.contour( img_IUV[:,:,1]/256., 10, linewidths = 1 )
    plt.contour( img_IUV[:,:,2]/256., 10, linewidths = 1 )
    plt.axis('off')
    #plt.show()
    out_full_file = os.path.join( args.results_dir, os.path.basename(args.in_image_IUV).split("_IUV.")[0] + "_IUV_contour.png" )
    plt.savefig( out_full_file, dpi = 100, bbox_inches = 'tight' )
