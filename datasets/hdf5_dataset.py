import h5py
import numpy as np
import torch
from torchvision import transforms


class ThreeDMAD(torch.utils.data.Dataset):
    """
        3DMAD dataset: https://gitlab.idiap.ch/bob/bob.db.maskattack/-/tree/master/doc
    """
    def parse_label_by_name(hdf5_name):
        if 'attack' in hdf5_name.lower():
            return 3
        elif 'bonafide' in hdf5_name.lower():
            return 0


    def __init__(self, h5_path, face_label=0, torchvision_transform=None, num_frames=1000):
        self.h5_path = h5_path
        self.face_label = face_label

        # Keys: ['Color_Data', 'Depth_Data', 'Eye_Pos']>
        self.h5_dataset = h5py.File(self.h5_path, 'r')

        len_dataset = self.h5_dataset['Eye_Pos'].shape[0]
        self.index_list = list(range(len_dataset))

        if torchvision_transform is None:
            self.transform = transforms.ToTensor()
        else:
            self.transform = torchvision_transform

        if len(self.index_list) > num_frames:
            sample_indices = np.linspace(0, len(self.index_list) - 1, num=num_frames, dtype=int)
            self.index_list = [self.index_list[id] for id in sample_indices]

        self.len = len(self.index_list)

    def get_image(self, index):
        color_data = self.h5_dataset['Color_Data'][index]  # (3,480,640), unit, RGB
        return color_data.transpose((1, 2, 0))  # (480,640,3)

    def __getitem__(self, index):
        idx = self.index_list[index]

        im = self.get_image(idx)
        img_tensor = self.transform(im)
        img_tensor = img_tensor.to(torch.float)
        target = self.face_label
        return index, img_tensor, target, self.h5_path

    def __len__(self):
        return self.len


class CSMAD(torch.utils.data.Dataset):

    def parse_label_by_name(hdf5_name):
        if 'attack' in hdf5_name.lower():
            return 3
        elif 'bonafide' in hdf5_name.lower():
            return 0

    def __init__(self, h5_path, face_label, torchvision_transform=None, num_frames=1000):
        self.h5_path = h5_path
        self.face_label = face_label
        # Keys: ['Color_Data', 'Depth_Data', 'Eye_Pos']>
        self.h5_dataset = h5py.File(self.h5_path, 'r')
        self.key_list = list(self.h5_dataset['data']['sr300']['infrared'].keys())

        if len(self.key_list) > num_frames:
            sample_indices = np.linspace(0, len(self.key_list) - 1, num=num_frames, dtype=int)
            self.key_list = [self.key_list[id] for id in sample_indices]

        if torchvision_transform is None:
            self.transform = transforms.ToTensor()
        else:
            self.transform = torchvision_transform

        self.len = len(self.key_list)

    def get_image(self, index):
        key = self.key_list[index]
        color_data = self.h5_dataset['data']['sr300']['color'][key][:]  # (640,830, 3) unit8
        return color_data
    def __getitem__(self, index):


        # ir_data = self.h5_dataseta['data']['seek_compact']['infrared']['09_35_58_990']
        # depth_data = self.h5_dataset['Depth_Data'][index] # (1,480,640), uint8
        # ir_data = self.h5_dataset['data']['sr300']['infrared'][key][:] # (640,830) uint16
        # depth_data = self.h5_dataset['data']['sr300']['depth'][key][:] # (640,830) uint16

        im = self.get_image(index)

        img_tensor = self.transform(im).to(torch.float)
        target = self.face_label
        return index, img_tensor, target, self.h5_path

    def __len__(self):
        return self.len


class WMCA(torch.utils.data.Dataset):
    def parse_label_by_name(
            hdf5_name,
            bonafide_list_csv='/home/Dataset/Face_Spoofing/WMCA/WMCA_preprocessed_RGB/WMCA/documentation/bonafide_illustration_files.csv',
            attack_list_csv='/home/Dataset/Face_Spoofing/WMCA/WMCA_preprocessed_RGB/WMCA/documentation/attack_illustration_files.csv'
    ):

        with open(bonafide_list_csv) as f:
            bonafide_list = f.read()

        with open(attack_list_csv) as f:
            attack_list = f.read()

        if hdf5_name in bonafide_list:
            return 0

        elif hdf5_name in attack_list:
            return 3


    def __init__(self, h5_path, face_label, torchvision_transform=None, num_frames=1000):
        self.h5_path = h5_path
        self.face_label = face_label
        self.h5_dataset = h5py.File(self.h5_path, 'r')
        self.key_list = [x for x in self.h5_dataset.keys()]

        # import pdb; pdb.set_trace()
        self.len = len(self.key_list)

        if torchvision_transform is None:
            self.transform = transforms.ToTensor()
        else:
            self.transform = torchvision_transform

    def get_image(self, index):
        key = self.key_list[index]
        color_data = self.h5_dataset[key]['array'][:]  # (3, 128,128) unit8
        # import pdb; pdb.set_trace()
        color_data = np.transpose(color_data, (1,2,0))
        return color_data

    def __getitem__(self, index):
        # key = self.key_list[index]

        # ir_data = self.h5_dataseta['data']['seek_compact']['infrared']['09_35_58_990']
        # depth_data = self.h5_dataset['Depth_Data'][index] # (1,480,640), uint8
        # ir_data = self.h5_dataset['data']['sr300']['infrared'][key][:] # (640,830) uint16
        # depth_data = self.h5_dataset['data']['sr300']['depth'][key][:] # (640,830) uint16

        im = self.get_image(index)
        img_tensor = self.transform(im)
        target =  self.face_label

        return index, img_tensor, target, self.h5_path

    def __len__(self):
        return self.len


if __name__ == '__main__':
    # dataset = WMCA('/home/rizhao/data/FAS/wmca/ir/test/fake_head/505_01_000_2_06/', 0, None)
    dataset_3dmad = ThreeDMAD('/home/Dataset/Face_Spoofing/3DMAD/session01/Data/04_01_05.hdf5', 0, None)
    dataset_csmad = CSMAD('/home/Dataset/Face_Spoofing/CSMAD/attack/STAND/A/Mask_atk_A1_i0_001.h5', 0, None)
    dataset_wmca = WMCA(
        '/home/Dataset/Face_Spoofing/WMCA/WMCA_preprocessed_RGB/WMCA/face-station/31.01.18/514_01_035_1_05.hdf5',
        0, None)
    out1 = dataset_3dmad.__getitem__(0)
    out2 = dataset_csmad.__getitem__(0)
    out3 = dataset_wmca.__getitem__(0)
    import IPython;  IPython.embed()
