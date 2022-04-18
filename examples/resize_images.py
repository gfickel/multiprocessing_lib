import argparse
import glob
import os

import cv2

from doc_ock.mp_lock import mp_lock


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script to resize a batch of images')
    parser.add_argument('--images_path', type=str, required=True,
            help='Images path')
    parser.add_argument('--out_path', type=str, required=True,
            help='Output path')
    parser.add_argument('--num_procs', type=int, required=True,
            help='Number of processes')
    args = parser.parse_args()

    data_list = glob.glob(args.images_path+'/*')

    def process(im_path):
        im = cv2.imread(im_path)
        if im is None:
            print('problem with image', im_path)
            return None
        im = cv2.resize(im, (224, 224), interpolation=cv2.INTER_AREA)
        cv2.imwrite(f'{args.out_path}/{os.path.basename(im_path)}', im)

    mp_lock(data_list, process, None, args.num_procs, args.out_path)
