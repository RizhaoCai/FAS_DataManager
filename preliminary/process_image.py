import logging

logging.level = logging.ERROR

import zipfile
import io
from glob import glob
from multiprocessing import Pool

import argparse
import sys
sys.path.append('mxnet_mtcnn_face_detection')

import sys
import mxnet as mx
from mxnet_mtcnn_face_detection.mtcnn_detector import MtcnnDetector
import cv2
import os
import numpy as np
import pdb


# ==================================Build detector =========================================================

detector = MtcnnDetector(model_folder='mxnet_mtcnn_face_detection/model', ctx=mx.cpu(0), num_worker=1,
                         accurate_landmark=False)

def detect_face_and_save_landmarks(image_name, image_frame=None, landmark_file_suffix="_bbox_mtccnn.txt"):
    global detector
    if image_frame is None:
        image_frame = cv2.imread(image_name)

    results = detector.detect_face(image_frame)
    if results is not None:
        total_boxes = results[0][0].astype(np.int32)
        points = results[1][0].astype(np.int32)

        # if height > args.max_size or width > args.max_size:
        #    pass
        # save crop
        str_to_write = ""
        #if total_boxes[0]<=0 or total_boxes[1]<=0 or total_boxes[2] <=0 or total_boxes[3]<=0:
        #    import pdb; pdb.set_trace()
        str_to_write += "{},{},{},{},{}".format(total_boxes[0], total_boxes[1], total_boxes[2], total_boxes[3],
                                                total_boxes[4])
        str_to_write += "\n"
        str_to_write += "{},{},{},{},{},{},{},{},{},{}".format(points[0], points[1], points[2], points[3], points[4],
                                                               points[5], points[6], points[7], points[8], points[9])
        # string_boxes = "%d\t%d" % (face_count, frame_count)
        bbox_info_file_path = image_name.replace('.png', landmark_file_suffix)
        print('Write bbox info to ', bbox_info_file_path)
        with open(bbox_info_file_path, 'w') as f:
            f.write(str_to_write)

def detect_and_align(img, desired_size=256):
    global detector
    results = detector.detect_face(img)

    total_boxes = results[0]
    points = results[1]

    # extract aligned face chips
    chips = detector.extract_image_chips(img, points, desired_size, 0.37)
    return chips[0]
# ==========================================================================================================

def process_one_image(input_fn_path):
    # get the input_fn ext_ratio

    # init VideoCapture
    image = cv2.imread(input_fn_path)
    height, width = image.shape[0], image.shape[1]
    detect_face_and_save_landmarks(input_fn_path, image)





def main(args):
    dataset_name = args.dataset
    matching_pattern = DATASET_DIR[dataset_name]
    print(matching_pattern)
    global ROOT_DIR
    image_fns = glob(os.path.join(ROOT_DIR,matching_pattern))

    num_workers = args.num_workers
    if num_workers > 1:
        pool = Pool(num_workers)
        pool.map(process_one_image, image_fns)

    else:
        i = 1
        # import pdb; pdb.set_trace()
        for fns in image_fns:
            print("Image {}/{}".format(i, len(image_fns)))
            process_one_image(fns)
            i += 1


if __name__ == "__main__":

    DATASET_DIR = {
        'CelabA-Spoof': 'CelabA-Spoof/*/*/*/*.png',  # e.g. CelabA-Spoof/test/9994/spoof/*.png

    }

    parser = argparse.ArgumentParser("Args parser for training")
    parser.add_argument("--num_workers", type=int, default=1, help="number of threads in the pools")
    parser.add_argument("--max_size", type=int, default=512, help="The maximum size")
    parser.add_argument("--dataset", type=str, default='CelabA-Spoof', help="Dataset name keys")
    parser.add_argument("--enable_mtcnn", action='store_true', help="The maximum size")
    parser.add_argument("--root_dir", default='/home/Dataset/Face_Spoofing/')

    args = parser.parse_args()
    ROOT_DIR = args.root_dir

    main(args)
