import torch
import numpy as np
import cv2
import os
import h5py


class WMCA(torch.utils.data.Dataset):
    """
        Also work for CASIA-SURF
    """

    def __init__(self, folder_path, face_label, transform, num_frames=1000):
        self.folder_path = folder_path
        self.transform = transform
        self.face_label = face_label

        self.image_list = os.listdir(self.folder_path)
        if len(self.image_list) > num_frames:
            sample_indices = np.linspace(0, len(self.image_list) - 1, num=num_frames, dtype=int)
            self.image_list = [self.image_list[id] for id in sample_indices]

        self.image_list = [os.path.join(folder_path, x) for x in self.image_list]
        self.len = len(self.image_list)

    def __getitem__(self, index):
        im = cv2.imread(self.image_list[index])
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        # im = im.transpose((2,0,1))
        tensor = self.transform(im)
        tensor = tensor.to(torch.float)
        target = {
            'face_label': self.face_label
        }
        return index, tensor, target, self.zip_file_path

    def __len__(self):
        return self.len


class ThreeDMAD(torch.utils.data.Dataset):
    def __init__(self, h5_path, face_label, transform, num_frames=1000):
        self.h5_path = h5_path
        self.transform = transform
        self.face_label = face_label

        # Keys: ['Color_Data', 'Depth_Data', 'Eye_Pos']>
        self.h5_dataset = h5py.File(self.h5_path, 'r')

        len_dataset = self.h5_dataset['Eye_Pos'].shape[0]
        self.index_list = list(range(len_dataset))
        if len(self.index_list) > num_frames:
            sample_indices = np.linspace(0, len(self.index_list) - 1, num=num_frames, dtype=int)
            self.index_list = [self.index_list[id] for id in sample_indices]

        self.len = len(self.index_list)

    def __getitem__(self, index):
        index = self.index_list[index]

        color_data = self.h5_dataset['Color_Data'][index]  # (3,480,640), uint8
        # depth_data = self.h5_dataset['Depth_Data'][index] # (1,480,640), uint8

        im = color_data.transpose((2, 0, 1))  # (480,640,3)
        tensor = self.transform(im)
        tensor = tensor.to(torch.float)
        target = {
            'face_label': self.face_label
        }

        return index, tensor, target, self.zip_file_path

    def __len__(self):
        return self.len


class CSMAD(torch.utils.data.Dataset):
    def __init__(self, h5_path, face_label, transform, num_frames=1000):
        self.h5_path = h5_path
        self.transform = transform
        self.face_label = face_label

        # Keys: ['Color_Data', 'Depth_Data', 'Eye_Pos']>
        self.h5_dataset = h5py.File(self.h5_path, 'r')

        self.key_list = list(self.h5_dataset['data']['sr300']['infrared'].keys())

        if len(self.key_list) > num_frames:
            sample_indices = np.linspace(0, len(self.key_list) - 1, num=num_frames, dtype=int)
            self.key_list = [self.key_list[id] for id in sample_indices]

        self.len = len(self.key_list)

    def __getitem__(self, index):
        key = self.key_list[index]

        # ir_data = self.h5_dataseta['data']['seek_compact']['infrared']['09_35_58_990']
        # depth_data = self.h5_dataset['Depth_Data'][index] # (1,480,640), uint8
        # ir_data = self.h5_dataset['data']['sr300']['infrared'][key][:] # (640,830) uint16
        # depth_data = self.h5_dataset['data']['sr300']['depth'][key][:] # (640,830) uint16
        color_data = self.h5_dataset['data']['sr300']['color'][key][:]  # (640,830, 3) unit8
        im = color_data

        tensor = self.transform(im)
        tensor = tensor.to(torch.float)
        target = {
            'face_label': self.face_label
        }
        return index, tensor, target, self.zip_file_path

    def __len__(self):
        return self.len


class WMCA_H5(torch.utils.data.Dataset):
    def __init__(self, h5_path, face_label, transform, num_frames=1000):
        self.h5_path = h5_path
        self.transform = transform
        self.face_label = face_label

        # Keys: ['Color_Data', 'Depth_Data', 'Eye_Pos']>
        self.h5_dataset = h5py.File(self.h5_path, 'r')

        self.len = len(self.h5_dataset.keys())

    def __getitem__(self, index):
        # key = self.key_list[index]

        # ir_data = self.h5_dataseta['data']['seek_compact']['infrared']['09_35_58_990']
        # depth_data = self.h5_dataset['Depth_Data'][index] # (1,480,640), uint8
        # ir_data = self.h5_dataset['data']['sr300']['infrared'][key][:] # (640,830) uint16
        # depth_data = self.h5_dataset['data']['sr300']['depth'][key][:] # (640,830) uint16
        key = 'Frame_{}'.format(index)
        color_data = self.h5_dataset[key]['array'][:]  # (640,830, 3) unit8
        im = color_data

        # tensor = self.transform(im)
        tensor = torch.from_numpy(im).to(torch.float)
        target = {
            'face_label': self.face_label
        }
        return index, tensor, target, self.h5_path

    def __len__(self):
        return self.len


if __name__ == '__main__':
    # dataset = WMCA('/home/rizhao/data/FAS/wmca/ir/test/fake_head/505_01_000_2_06/', 0, None)
    # dataset_3dmad = _3DMAD('/home/Dataset/FaceAntiSpoofing/3DMAD/session01/Data/04_01_05.hdf5', 0, None)
    # dataset_csmad = CSMAD('/home/Dataset/FaceAntiSpoofing/CSMAD/attack/STAND/A/Mask_atk_A1_i0_001.h5', 0, None)
    dataset_wmca = WMCA_H5(
        '/home/Dataset/FaceAntiSpoofing/WMCA/WMCA_preprocessed_RGB/WMCA/preprocessed-face-station_RGB/31.01.18/514_01_035_1_05.hdf5',
        0, None)

    import pdb;

    pdb.set_trace()
