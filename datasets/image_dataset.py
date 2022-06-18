import os
import cv2
import torch

class WFDD:
    def __init__(self, image_folder_dir, face_label, transform, num_frames=1000):

        os.listdir(image_folder_dir)
        image_list = os.listdir(image_folder_dir)
        self.image_list = [os.path.join(image_folder_dir, p) for p in image_list]
        self.face_label = face_label


    def __getitem__(self, index):
        im = self.__read_image__(index) # cv2 image, format [H, W, C], BGR
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        # im = im.transpose((2,0,1))
        tensor = self.transform(im)
        tensor = tensor.to(torch.float)
        target = {
            'face_label':  self.face_label
        }
        return index, tensor, target, self.zip_file_path


class CASIA_HIFI_MASK:
    def __init__(self, image_folder_dir, face_label, transform, num_frames=1000):
        image_list = os.listdir(image_folder_dir)
        self.image_list = [ os.path.join(image_folder_dir,p) for p in image_list]
        self.face_label = face_label
    def __getitem__(self, index):

        path = self.image_list[index]
        im = cv2.imread(path)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

        # im = im.transpose((2,0,1))
        tensor = self.transform(im)
        tensor = tensor.to(torch.float)
        target = {
            'face_label': self.face_label
        }
        return index, tensor, target, path


class CASIA_SURF:
    def __init__(self, image_folder_dir, face_label, transform, num_frames=1000):
        image_list = os.listdir(image_folder_dir)
        self.image_list = [ os.path.join(image_folder_dir,p) for p in image_list]
        self.face_label = face_label
    def __getitem__(self, index):

        path = self.image_list[index]
        im = cv2.imread(path)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

        # im = im.transpose((2,0,1))
        tensor = self.transform(im)
        tensor = tensor.to(torch.float)
        target = {
            'face_label': self.face_label
        }
        return index, tensor, target, path