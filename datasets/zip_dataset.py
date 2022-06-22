"""
 This is used when video frames are extracted and packed in a zip, which can help the reduce the management burden due to a large
 number of the small files. But this also leads to more inconvenience in the programming. As for research purposes, it is
 more convenient to extract frames and save the frames as images under folders.
"""
import cv2
import numpy as np
import torch
import zipfile



class ZipDataset(torch.utils.data.Dataset):
    def __init__(self, zip_file_path, face_label, transform, num_frames=1000, use_original_frame=False, bbox_suffix='_mtccnn.txt'):
        """

        :param zip_file_path:
        :param face_label:
        :param transform: pytorch transform function
        :param num_frames:maximum frames to extract in this zip files
        :param use_original: If True, then grabbed image without cropping
        :param bbox_suffix:
        """
        self.zip_file_path = zip_file_path
        self.transform = transform
        self.decode_flag = cv2.IMREAD_UNCHANGED
        self.face_label = face_label

        self.image_list_in_zip = []
        with zipfile.ZipFile(self.zip_file_path, "r") as zip:
            lst = zip.namelist()
            exts = ['png', 'jpg']
            for ext in exts:
                self.image_list_in_zip += list(filter(lambda x: x.lower().endswith(ext), lst))

        if len(self.image_list_in_zip) > num_frames:
            sample_indices = np.linspace(0, len(self.image_list_in_zip)-1, num=num_frames, dtype=int)
            self.image_list_in_zip = [self.image_list_in_zip[id] for id in sample_indices]

        self.use_original_frame = use_original_frame
        self.bbox_suffix = bbox_suffix
        self.len = len(self.image_list_in_zip)



    def __read_image_from_zip__(self, index):
        image_name_in_zip = self.image_list_in_zip[index]
        with zipfile.ZipFile(self.zip_file_path, "r") as zip:
            bytes_ = zip.read(image_name_in_zip)
            bytes_ = np.frombuffer(bytes_, dtype=np.uint8)
            im = cv2.imdecode(bytes_, self.decode_flag)  # cv2 image

            if self.use_original_frame:
                return im
            else:
                # Crop face
                bbox_file_name = image_name_in_zip.replace('.png', self.bbox_suffix)
                bbox_info = zip.read(bbox_file_name)
                #import pdb;
                #pdb.set_trace()

                bboxes, landmark_points= str(bbox_info, 'utf-8').split()
                bboxes = bboxes.split(',')
                landmark_points = landmark_points.split(',')
                x1, y1, x2, y2 = int(bboxes[0]), int(bboxes[1]), int(bboxes[2]), int(bboxes[3])
                crop_face = im[y1:y2, x1:x2]
                import pdb; pdb.set_trace()
                # cv2.imwrite('test.png', crop_face)
                return crop_face

    def __getitem__(self, index):
        im = self.__read_image_from_zip__(index) # cv2 image, format [H, W, C], BGR
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        # im = im.transpose((2,0,1))
        tensor = self.transform(im)
        tensor = tensor.to(torch.float)
        target = {
            'face_label':  self.face_label
        }
        return index, tensor, target, self.zip_file_path

    def __len__(self):
        return self.len


if __name__ == '__main__':
    # Test example
    zip_file_path = '/home/rizhao/data/FAS/Version2/CASIA-FASD/test_release/1/1.avi.zip'
    dataset = ZipDataset(zip_file_path, face_label=1, transform=None)
    x = dataset.__getitem__(1)
    import IPython; IPython.embed()




