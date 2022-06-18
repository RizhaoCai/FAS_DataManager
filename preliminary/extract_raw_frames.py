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

detector = MtcnnDetector(model_folder='mxnet_mtcnn_face_detection/model', ctx=mx.cpu(0), num_worker=8,
                         accurate_landmark=False)


def detect_and_align(img, desired_size=256):
    global detector
    results = detector.detect_face(img)

    total_boxes = results[0]
    points = results[1]

    # extract aligned face chips
    chips = detector.extract_image_chips(img, points, desired_size, 0.37)
    return chips[0]


ROOT_DIR = '/home/Dataset/Face_Spoofing/'  # Where you save the raw data you download
SAVE_DIR = '/home/rizhao/data/FAS/Version2/'  # Where you want to save the processed data

DATASET_DIR = {
    'OULU-NPU': 'OULU-NPU/*/*.avi',  #
    'CASIA-FASD': 'CASIA-FASD/*/*/*.avi',  #
    'REPLAY-ATTACK': 'REPLAY-ATTACK/*/*/*.mov',  #
    'REPLAY-ATTACK-SPOOF': 'REPLAY-ATTACK/*/*/*/*.mov',  #
    'SIW': 'SIW/*/*/*/*.mov',
    'ROSE-YOUTU': 'ROSE-YOUTU/*/*/*.mp4',  #
    'MSU-MFSD': 'MSU-MFSD/scene01/*/*.mp4',
    'MSU-MFSD2': 'MSU-MFSD/scene01/*/*.mov',
    'CASIA-SURF-3DMASK': 'CASIA_SURF_3DMask/*/*/*.MOV',
    'HKBU_MARs_V2': 'HKBU_MARs_V2/HKBU_MARs_V2/*/*/*.avi'
}


def process_one_video(input_fn):
    # get the input_fn ext_ratio
    global ROOT_DIR
    output_fn = os.path.relpath(input_fn, ROOT_DIR)
    output_fn = os.path.join(SAVE_DIR + output_fn + ".zip")
    output_folder_dir = os.path.dirname(output_fn)

    print('input_fn: ', input_fn)
    print("output_fn: ", output_fn)

    # skip if output_fn exists
    if os.path.exists(output_fn):
        print("output_fn exists, skip")
        return
    elif not os.path.exists(output_folder_dir):
        print('Create ', output_folder_dir)
        os.makedirs(output_folder_dir, exist_ok=True)

    # init VideoCapture
    cap = cv2.VideoCapture(input_fn)

    # get frame
    face_count = 0
    frame_count = 0

    with io.BytesIO() as bio:
        with zipfile.ZipFile(bio, "w") as zip:
            # write pngs to zip in memory
            for frame_idx in range(1000000000):
                success, frame = cap.read()
                if frame_idx > args.max_frames:
                    break
                if not success:
                    print("video ends")
                    assert frame is None
                    break
                height, width = frame.shape[0], frame.shape[1]

                frame_count += 1

                # rescale the bounding box
                # t = rect.top() / rescale
                # b = rect.bottom() / rescale
                # l = rect.left() / rescale
                # r = rect.right() / rescale
                # try:
                #    crop = mxnet_detector.detect_and_align(im, 256)
                #    face_count += 1
                zip_helper.write_im_to_zip(zip, str(frame_idx) + ".png", frame)

                results = detector.detect_face(frame)
                if results is not None:
                    total_boxes = results[0][0].astype(np.int)
                    points = results[1][0].astype(np.int)

                    #if height > args.max_size or width > args.max_size:
                    #    pass
                    # save crop
                    bytes_to_write = ""
                    bytes_to_write += "{},{},{},{},{}".format(total_boxes[0], total_boxes[1], total_boxes[2], total_boxes[3], total_boxes[4])
                    bytes_to_write+="\n"
                    bytes_to_write += "{},{},{},{},{},{},{},{},{},{}".format(points[0], points[1], points[2], points[3], points[4], points[5], points[6], points[7], points[8], points[9])
                    # string_boxes = "%d\t%d" % (face_count, frame_count)
                    zip_helper.write_bytes_to_zip(zip, "{}_mtccnn.txt".format(frame_idx), bytes(bytes_to_write, "utf-8"))

        # finally, flush bio to disk once
        path = os.path.dirname(output_fn)
        if path != "":
            os.makedirs(path, exist_ok=True)
        with open(output_fn, "wb") as f:
            f.write(bio.getvalue())

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

    parser = argparse.ArgumentParser("Args parser for training")
    parser.add_argument("--num_workers", type=int, default=1, help="number of threads in the pools")
    parser.add_argument("--max_size", type=int, default=512, help="The maximum size")
    parser.add_argument("--dataset", type=str, default='CASIA-FASD', help="The maximum size")
    parser.add_argument("--enable_mtcnn", action='store_true', help="The maximum size")
    parser.add_argument("--max_frames", type=int, default=10, help="The maximum size")

    args = parser.parse_args()

    main(args)
