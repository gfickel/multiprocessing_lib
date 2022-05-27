import os
import argparse
import glob

import cv2
import numpy as np

from faceattributes import face_detector, utils


# TODO: perhaps make a package in root will fix that.
import sys
sys.path.append("..")
from mp_lock import mp_lock

model = face_detector.FaceDetector()

FIELDS = ["filepath", "got_detection", "bbox_tl_x", "bbox_tl_y", "bbox_br_x", "bbox_br_y", \
                "l_0_x", "l_0_y", "l_1_x", "l_1_y", "l_2_x", "l_2_y", "l_3_x", "l_3_y", "l_4_x", "l_5_y"]

def get_args():
    parser = argparse.ArgumentParser(description='Call API')
    parser.add_argument('--num_procs', type=int, required=True,
            help='Number of processes')
    parser.add_argument('--input_images', type=str, required=True,
            help='Path to the input images')
    parser.add_argument('--out_path', type=str, required=True,
            help='Output path')
    return parser.parse_args()

def process(data):
    image_filepath = data

    img = cv2.imread(image_filepath)
    det_box, det_landmarks, det_confidence = model.detect_largest_face(img, thresholds=(0.725, 0.735, 0.75) )

    if not det_box:
        return None

    img_normalized = utils.align_face_224(img, det_landmarks[0])

    flatten_path = image_filepath.replace("/", "_")
    im_out_filepath = f"image_out/{flatten_path[:flatten_path.rfind('.')]}_normalized_face.png"
    cv2.imwrite(im_out_filepath, img_normalized)

    return {
        "bbox": det_box[0],
        "landmarks": det_landmarks[0],
        "confidence": det_confidence[0]
    }


def save_callback(output_filepath, data_results, data_names):

    def convert_data(filepath, res):

        if res is None:
            return [filepath, False] + [None]*(len(FIELDS)-2)

        face_res = list(res["bbox"][0]) + list(res["bbox"][0])
        face_land = res["landmarks"].flatten().tolist()
        return [filepath, True] + face_res + face_land

    print("data_results", data_results)
    print("data_names", data_names)
    with open(output_filepath+'.csv', 'a') as fid:
        for fn, res in zip(data_names, data_results):
            csv_values = convert_data(fn, res)
            csv_str_line = ",".join([str(x) if x is not None else "" for x in csv_values])
            fid.write(csv_str_line+"\n")


if __name__ == '__main__':
    args = get_args()
    images = glob.glob(f'{args.input_images}/**/*', recursive=True)
    valid_extensions = ('.jpg', '.png', '.jpeg')
    images = [x for x in images if os.path.isfile(x) and x.lower().endswith(valid_extensions)]
    print("init")
    mp_lock(images, process, save_callback, args.num_procs, args.out_path, 1)

