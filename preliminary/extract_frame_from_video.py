import logging

logging.level = logging.ERROR

import zipfile
import io
from glob import glob
from multiprocessing import Pool

import argparse
import sys
sys.path.append('mxnet_mtcnn_face_detection')
import misc.zip_helper as zip_helper

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

def detect_face_and_save_landmarks(image_name, image_frame=None):
    global detector
    if image_frame is None:
        image_frame = cv2.imread(image_name)

    results = detector.detect_face(image_frame)
    if results is not None:
        total_boxes = results[0][0].astype(np.int)
        points = results[1][0].astype(np.int)

        # if height > args.max_size or width > args.max_size:
        #    pass
        # save crop
        str_to_write = ""
        str_to_write += "{},{},{},{},{}".format(total_boxes[0], total_boxes[1], total_boxes[2], total_boxes[3],
                                                total_boxes[4])
        str_to_write += "\n"
        str_to_write += "{},{},{},{},{},{},{},{},{},{}".format(points[0], points[1], points[2], points[3], points[4],
                                                               points[5], points[6], points[7], points[8], points[9])
        # string_boxes = "%d\t%d" % (face_count, frame_count)
        bbox_info_file_path = image_name.replace('.png', "_bbox_mtccnn.txt")
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

def process_one_video(input_fn):
    # get the input_fn ext_ratio
    global ROOT_DIR
    output_fn = os.path.relpath(input_fn, ROOT_DIR)
    output_folder_dir = os.path.join(SAVE_DIR + output_fn)
    # output_folder_dir = os.path.dirname(output_fn)

    print('input_fn: ', input_fn)
    print("output_fn: ", output_folder_dir)

    # skip if output_fn exists
    if not os.path.exists(output_folder_dir):
        print('Create ', output_folder_dir)
        os.makedirs(output_folder_dir, exist_ok=True)

    # init VideoCapture
    cap = cv2.VideoCapture(input_fn)

    # get frame
    frame_count = 0

    for frame_idx in range(10000):
        success, frame = cap.read()

        if not success:
            print("video ends")
            assert frame is None
            break
        height, width = frame.shape[0], frame.shape[1]

        frame_count += 1
        if frame_count > args.max_frames:
            break

        img_save_path = os.path.join(output_folder_dir,"{}.png".format(frame_count))
        cv2.imwrite(img_save_path,frame)
        print('Write image to ', img_save_path)
        detect_face_and_save_landmarks(img_save_path, frame)

    cap.release()


def main(args):
    dataset_name = args.dataset
    matching_pattern = DATASET_DIR[dataset_name]
    print(matching_pattern)
    global ROOT_DIR
    video_fns = glob(os.path.join(ROOT_DIR,matching_pattern))

    num_workers = args.num_workers
    if num_workers > 1:
        pool = Pool(num_workers)
        pool.map(process_one_video, video_fns)

    else:
        i = 1
        # import pdb; pdb.set_trace()
        for fns in video_fns:
            print("Video {}/{}".format(i, len(video_fns)))
            process_one_video(fns)
            i += 1


if __name__ == "__main__":

    DATASET_DIR = {
        'OULU-NPU': 'OULU-NPU/*/*.avi',  #
        'CASIA-FASD': 'CASIA-FASD/*/*/*.avi',  #
        'REPLAY-ATTACK': 'REPLAY-ATTACK/*/*/*.mov',  #
        'REPLAY-ATTACK-SPOOF': 'REPLAY-ATTACK/*/*/*/*.mov',  #
        'SIW': 'SIW/*/*/*/*.mov',
        'ROSE-YOUTU': 'ROSE-YOUTU/*/*/*.mp4',  #
        'MSU-MFSD': 'MSU-MFSD/scene01/*/*.mp4',
        'MSU-MFSD2': 'MSU-MFSD/scene01/*/*.mov',
        'CASIA-SURF-3DMASK_REAL': 'CASIA_SURF_3DMask/Real/*/*.MOV',
        'CASIA-SURF-3DMASK_FAKE': 'CASIA_SURF_3DMask/Fake/*/*/*.MOV',
        'HKBU_MARs_V2': 'HKBU_MARs_V2/HKBU_MARs_V2/*/*/*.avi'
    }

    parser = argparse.ArgumentParser("Args parser for training")
    parser.add_argument("--num_workers", type=int, default=1, help="number of threads in the pools")
    parser.add_argument("--max_size", type=int, default=512, help="The maximum size")
    parser.add_argument("--dataset", type=str, default='CASIA-FASD', help="Dataset name keys")
    parser.add_argument("--enable_mtcnn", action='store_true', help="The maximum size")
    parser.add_argument("--max_frames", type=int, default=10, help="The maximum frame to extract")
    parser.add_argument("--root_dir", default='/home/Dataset/Face_Spoofing/')
    parser.add_argument("--save_dir", default='/home/rizhao/data/FAS/frames/')

    args = parser.parse_args()
    ROOT_DIR = args.root_dir
    SAVE_DIR = args.save_dir

    main(args)
