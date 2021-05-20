import os
import argparse
import numpy
import cv2
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--in_image_dir", default="results/sample_n5/iuv/")
    parser.add_argument("--results_dir", default="results/sample_n5/segument/")
    parser.add_argument('--image_height', type=int, default=256)
    parser.add_argument('--image_width', type=int, default=192)
    parser.add_argument('--format', choices=['contour', 'segument'], default='segument')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    if( args.debug ):
        for key, value in vars(args).items():
            print('%s: %s' % (str(key), str(value)))

    if not os.path.isdir(args.results_dir):
        os.mkdir(args.results_dir)

    image_names = sorted( [f for f in os.listdir(args.in_image_dir) if f.endswith("_IUV.png")] )
    for img_name in tqdm(image_names):
        img_IUV = cv2.imread( os.path.join(args.in_image_dir, img_name) )
        if( args.format == "contour" ):
            fig = plt.figure(figsize=[args.image_width/100,args.image_height/100])
            plt.contour( img_IUV[:,:,1]/256., 10, linewidths = 1 )
            plt.contour( img_IUV[:,:,2]/256., 10, linewidths = 1 )
            plt.axis('off')
            #plt.show()
            out_full_file = os.path.join( args.results_dir, os.path.basename(os.path.join(args.in_image_dir, img_name)).split("_IUV.")[0] + "_IUV_contour.png" )
            plt.savefig( out_full_file, dpi = 100, bbox_inches = 'tight' )

        elif( args.format == "segument" ):
            img_IUV_parse = img_IUV[:,:,0]
            out_full_file = os.path.join( args.results_dir, os.path.basename(os.path.join(args.in_image_dir, img_name)).split("_IUV.")[0] + "_IUV_segument.png" )
            cv2.imwrite(out_full_file, img_IUV_parse)