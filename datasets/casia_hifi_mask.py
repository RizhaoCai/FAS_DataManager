"""
Function: Load Data for Face Anti-spoofing According to Defined Protocols
Author: AJ
Date: 2021/1/15
"""
import os, glob, torch, cv2, copy

import re

class CASIA_HiFiMask:
    def parse_label_by_name(path):

        meta_info = {}
        """
            Name: ComplexionID_SubjectID_TypeID_SceneID_LightID_SensorID
            Complexion: Yellow(1), White(2), Black(3)
            Subject: 01, 02, 03, ... , 75
            Type: Live(0), Transparent(1), Plaster(2), Resin(3)
            Scene: White(1), Green(2), Tricolor(3), Sunshine(4), Shadow(5), Motion(6)
            Light: No(0), NormalLight(1), DimLight(2), BrightLight(3), BacklitLight(4),  SideSight(5), TopLight(6)
            Sensor: SpO2(0), Iphone11(1), IphoneX(2), MI10(3), P40(4), S20(5), Vivo(6), D435(7), HJIM(8)
        """
        unit_name = re.search(path, '(\d+)_(\d+)_(\d+)_(\d+)_(\d+)_(\d+)')[0]
        subject_id, type_id, scene_id, light_id, sensor_id = unit_name.split('_')

        if int(type_id) == 0:
            label = 0
        else:
            # Different masks are labled as 3
            return 3

    def __init__(self, protocol, phase):
        """
        :param file_list: all videos
        :param protocol:
        :param phase: 'train', 'dev', 'test'
        Name: ComplexionID_SubjectID_TypeID_SceneID_LightID_SensorID.video
        Complexion: Yellow(1), White(2), Black(3)
        Subject: 01, 02, 03, ... , 75
        Type: Live(0), Transparent(1), Plaster(2), Resin(3)
        Scene: White(1), Green(2), Tricolor(3), Sunshine(4), Shadow(5), Motion(6)
        Light: No(0), NormalLight(1), DimLight(2), BrightLight(3), BacklitLight(4),  SideSight(5), TopLight(6)
        Sensor: SpO2(0), Iphone11(1), IphoneX(2), MI10(3), P40(4), S20(5), Vivo(6), D435(7), HJIM(8)
        All Sensors:  75*4*(4*6*8 + 2*8) = 75*4*208 = 75*832 = 62400
        Remove(D435): 75*4*(4*6*7 + 2*7) = 75*4*182 = 75*728 = 54600
        zip -P cbsr_wanjun_62903 -s 18432m -r CASIA-Mask-Video.zip CASIA-Mask-Video
        cat CASIA-HiFi-Mask.z* > CASIA-HiFi-Mask-Frame.zip
        or 7za x xxx.zip -o./tmp/
        """
        protocol_dict = {}
        protocol_dict['HiFiMask_p1'] = {
            'train': {
                'ComplexionID': [1, 2, 3],
                'SubjectID': list(range(1, 16)),
                'TypeID': [0, 1, 2, 3],
                'SceneID': [1, 2, 3, 4, 5, 6],
                'LightID': [0, 1, 2, 3, 4, 5, 6],
                'SensorID': [0, 1, 2, 3, 4, 5, 6, 7, 8]
                },
            'dev': {
                'ComplexionID': [1, 2, 3],
                'SubjectID': list(range(16, 18)),
                'TypeID': [0, 1, 2, 3],
                'SceneID': [1, 2, 3, 4, 5, 6],
                'LightID': [0, 1, 2, 3, 4, 5, 6],
                'SensorID': [0, 1, 2, 3, 4, 5, 6, 7, 8]
            },
            'test': {
                'ComplexionID': [1, 2, 3],
                'SubjectID': list(range(18, 26)),
                'TypeID': [0, 1, 2, 3],
                'SceneID': [1, 2, 3, 4, 5, 6],
                'LightID': [0, 1, 2, 3, 4, 5, 6],
                'SensorID': [0, 1, 2, 3, 4, 5, 6, 7, 8]
            }
        }

        for i in range(3):
            protocol_dict['HiFiMask_p2@%d' % (i + 1)] = copy.deepcopy(protocol_dict['HiFiMask_p1'])
            protocol_dict['HiFiMask_p2@%d' % (i + 1)]['train']['TypeID'] = [0]
            protocol_dict['HiFiMask_p2@%d' % (i + 1)]['dev']['TypeID'] = [0]
            protocol_dict['HiFiMask_p2@%d' % (i + 1)]['test']['TypeID'] = [0]
            for j in range(3):
                if j == i:
                    protocol_dict['HiFiMask_p2@%d' % (i + 1)]['test']['TypeID'].append(j + 1)
                else:
                    protocol_dict['HiFiMask_p2@%d' % (i + 1)]['train']['TypeID'].append(j + 1)
                    protocol_dict['HiFiMask_p2@%d' % (i + 1)]['dev']['TypeID'].append(j + 1)

        protocol_dict['HiFiMask_p3'] = {
            'train': {
                'ComplexionID': [1],
                'SubjectID': list(range(1, 16)),
                'TypeID': [0, 1, 2],
                'SceneID': [1],
                'LightID': [0, 1],
                'SensorID': [0, 1, 2]
            },
            'dev': {
                'ComplexionID': [1],
                'SubjectID': list(range(16, 18)),
                'TypeID': [0, 1, 2],
                'SceneID': [1],
                'LightID': [0, 1],
                'SensorID': [0, 1, 2]
            },
            'test': {
                'ComplexionID': [2, 3],
                'SubjectID': list(range(18, 26)),
                'TypeID': [0, 3],
                'SceneID': [2, 3, 4, 5, 6],
                'LightID': [2, 3, 4, 5, 6],
                'SensorID': [3, 4, 5, 6, 7, 8]
            }
        }

        protocol_dict['HiFiMask_p3'] = {}

        if not (protocol in protocol_dict.keys()):
            print('Error:{}, Protocal should in:{}'.format(protocol, list(protocol_dict.keys())))
            exit(1)
        self.protocol = protocol
        self.phase = phase
        self.protocol_info = protocol_dict[protocol][phase]

    def isInPotocol(self, video):
        ComplexionID, SubjectID, TypeID, SceneID, LightID, SensorID = video.split('_')
        if (int(ComplexionID) in self.protocol_info['ComplexionID']) \
        and (int(SubjectID) in self.protocol_info['SubjectID']) \
        and (int(TypeID) in self.protocol_info['TypeID']) \
        and (int(SceneID) in self.protocol_info['SceneID']) \
        and (int(LightID) in self.protocol_info['LightID']) \
        and (int(SensorID) in self.protocol_info['SensorID']):
            return True
        else:
            return False

    def dataset_process(self, tmp_videos, videos):
        get_videos = []
        for i in range(0, len(tmp_videos)):
            if self.isInPotocol(tmp_videos[i]):
                get_videos.append(videos[i])
        print('********** Dataset Info **********')
        print('Data:CASIA-HiFiMask, protocol:{}, Mode:{}'.format(self.protocol, self.phase))
        print('All videos={} vs Protocal videos={}'.format(len(tmp_videos), len(get_videos)))
        print('**********************************')
        return get_videos

class ImageClass():
    """
    Stores the paths of images for a given video
    input: video_name, image_paths
    output: class(include three functions)
    """
    def __init__(self, name, image_paths):
        self.name = name
        self.image_paths = image_paths
    def __str__(self):
        return self.name + ', ' + str(len(self.image_paths)) + ' images'
    def __len__(self):
        return len(self.image_paths)

def Load_CASIA_HiFiMask(data_root, protocol, phase, modal=''):
    """
    CASIA-SURF HiFiMask(High-Fidelity Mask)
    :param protocol:
    :param phase: 'train', 'dev', 'test'
    """
    dataset = []
    all_folders = glob.glob(os.path.join(data_root, '*'))
    videos = []
    tmp_videos = []
    for folder in all_folders:
        pure_folder = folder.split('/')[-1]
        if 'Info' in pure_folder:continue
        ComplexionID, SubjectID, TypeID, SceneID, LightID, SensorID = pure_folder.split('_')
        if SensorID == '0':continue
        videos.append(folder)
        _, new_SubjectID, _ = subject_dict[SubjectID].split('_')
        tmp_video = '_'.join([ComplexionID, new_SubjectID, TypeID, SceneID, LightID, SensorID])
        tmp_videos.append(tmp_video)
    ### Get according videos
    get_videos = CASIA_HiFiMask(protocol, phase).dataset_process(tmp_videos, videos)
    for video in get_videos:
        image_paths = glob.glob(os.path.join(video, modal, '*' + '.png'))
        assert len(image_paths) >= 10
        dataset.append(ImageClass(video, image_paths))
    return dataset

### <Live:label==0, fake:label==1> (training)
def video_2_label(video_name, data_name='HiFiMask'):
    if data_name == 'HiFiMask':
        label = int(video_name.split('_')[-4])
        label = 0 if label == 0 else 1
    else:
        label = int(video_name.split('_')[-1])
        label = 0 if label == 1 else 1
    return label

def get_sframe_paths_labels(dataset, phase, num='one', ratio=1):
    image_paths_flat = []
    labels_flat = []
    for i in range(len(dataset)):
        label = video_2_label(dataset[i].name)
        if phase == 'train':
            if label == 0:ratio_ = 1  ### live
            else:ratio_ = ratio       ### fake
            sample_image_paths = \
                [dataset[i].image_paths[sam_idx] for sam_idx in range(0, len(dataset[i].image_paths), ratio_)]
            image_paths_flat += sample_image_paths
            labels_flat += [label] * len(sample_image_paths)
        elif (phase == 'dev') or (phase == 'test'):
            if num == 'one':load_num = 1
            elif num == 'all':load_num = len(dataset[i].image_paths)
            ### image_paths_flat += random.sample(dataset[i].image_paths, batch_size_val)
            image_paths_flat += dataset[i].image_paths[0:0 + load_num] ### In order to get stable results
            labels_flat += [label] * load_num
    assert len(image_paths_flat) == len(labels_flat)
    return image_paths_flat, labels_flat

# class Load_RGB_Queue(data.Dataset):
#     def __init__(self, image_list, label_list,
#                  image_size, mean_div, modals, phase, augumentor, seed,
#                  data_augment=[0, 0, 0, 0, 0], color_para=[8, 0.2, 0.05]):
#         super(Load_RGB_Queue, self).__init__()
#         self.image_list = image_list
#         self.label_list = label_list
#         self.image_size = image_size
#         self.mean_div = mean_div
#         self.modals = modals
#         self.phase = phase
#         self.augumentor = augumentor
#         self.seed = seed
#         #####################
#         self.max_angle, self.RANDOM_FLIP, self.RANDOM_CROP, self.RANDOM_COLOR, self.is_std = \
#             data_augment[0], data_augment[1], data_augment[2], data_augment[3], data_augment[4]
#         self.c_alpha, self.c_beta, self.c_gamma = int(color_para[0]), color_para[1], color_para[2]
#         self.num_data = len(image_list)
#
#     def __len__(self):
#         return self.num_data
#
#     def __getitem__(self, index):
#         head_filename, label = self.image_list[index], self.label_list[index]
#
#     ####### color ########
#         color_image = cv2.imread(head_filename)  # BGR + HWC
#         color_image = cv2.resize(color_image, self.image_size, interpolation=cv2.INTER_CUBIC)
#         color_image = self.augumentor(self.phase, color_image)
#         color_image = np.transpose(color_image, (2, 0, 1))  # HWC-CHW
#         color_image = (color_image - self.mean_div[0]) / self.mean_div[1]
#         label = int(label)
#         # print('index={}, head_filename={}, angle={}, label={}'.format(index, head_filename, angle, label))
#         return torch.FloatTensor(color_image), torch.LongTensor(np.asarray(label).reshape([-1]))
#
# def save_input_images(input_batch, SptiTemp, label_batch, mean_div, output_path, phase, epoch_iter):
#     """
#     save input images
#     """
#     save_path = os.path.join(output_path, phase)
#     if epoch_iter % 500 != 0:
#         return None
#     for bat in range(input_batch.shape[0]):       ### ((10, 9, 256, 256), (10, 1))
#         images = input_batch[bat].numpy()
#         images = np.transpose(images, (1, 2, 0))  ### CHW - HWC
#         num_modal = images.shape[-1] / 3
#         images = np.split(images, indices_or_sections=num_modal, axis=-1)
#         for idx in range(len(images)):
#             image = images[idx]
#             ### show way1
#             # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#             # from scipy import misc
#             # misc.imsave(os.path.join(save_path,
#             #     'epoch_iter({})_batch_iter({})_label({})_modal({}).png'.format(
#             #      epoch_iter, bat, label_batch[bat][0], idx)), image)
#             ### show way2
#             image = image * mean_div[1] + mean_div[0]
#             cv2.imwrite(os.path.join(save_path,
#                 'epoch_iter({})_batch_iter({})_label({})_modal({})_SD_{}.png'.format(
#                 epoch_iter, bat, label_batch[bat][0], idx, SptiTemp)), image)
#
# #######################################################################
# ### key(Day): value(Complexion_Subject_Gender)
# subject_dict = {
#     '06': '1_01_1',
#     '07': '1_02_1',
#     '08': '1_03_1',
#     '18': '1_04_1',
#     '12': '1_05_1',
#     '10': '1_06_1',
#     '13': '1_07_1',
#     '83': '1_08_1',
#     '19': '1_09_0',
#     '20': '1_10_0',
#     '21': '1_11_0',
#     '22': '1_12_0',
#     '23': '1_13_0',
#     '24': '1_14_0',
#     '25': '1_15_0',
#     '05': '1_16_1',
#     '17': '1_17_0',
#     '01': '1_18_1',
#     '02': '1_19_1',
#     '03': '1_20_1',
#     '04': '1_21_1',
#     '11': '1_22_0',
#     '14': '1_23_0',
#     '15': '1_24_0',
#     '16': '1_25_0',
#     '54': '2_01_1',
#     '55': '2_02_1',
#     '56': '2_03_1',
#     '76': '2_04_1',
#     '77': '2_05_1',
#     '78': '2_06_1',
#     '70': '2_07_1',
#     '72': '2_08_1',
#     '69': '2_09_0',
#     '71': '2_10_0',
#     '73': '2_11_0',
#     '74': '2_12_0',
#     '75': '2_13_0',
#     '79': '2_14_0',
#     '80': '2_15_0',
#     '51': '2_16_1',
#     '66': '2_17_0',
#     '28': '2_18_1',
#     '35': '2_19_1',
#     '36': '2_20_1',
#     '42': '2_21_1',
#     '27': '2_22_0',
#     '30': '2_23_0',
#     '37': '2_24_0',
#     '41': '2_25_0',
#     '52': '3_01_1',
#     '53': '3_02_1',
#     '59': '3_03_1',
#     '26': '3_04_1',
#     '31': '3_05_1',
#     '34': '3_06_1',
#     '40': '3_07_1',
#     '65': '3_08_1',
#     '64': '3_09_0',
#     '81': '3_10_0',
#     '82': '3_11_0',
#     '32': '3_12_0',
#     '33': '3_13_0',
#     '39': '3_14_0',
#     '45': '3_15_0',
#     '49': '3_16_1',
#     '63': '3_17_0',
#     '43': '3_18_1',
#     '46': '3_19_1',
#     '47': '3_20_1',
#     '48': '3_21_1',
#     '50': '3_22_0',
#     '57': '3_23_0',
#     '58': '3_24_0',
#     '61': '3_25_0',
# }
#
# #######################################
# ###        Data_Augment
# #######################################
# class Data_Augment(object):
#     def __init__(self, seq_index):
#         self.seq_index = seq_index
#         self.augumentor = self._augumentor
#     def _augumentor(self, phase, image):
#         if phase == 'train':
#             image = self.get_seq(self.seq_index).augment_image(image)
#             return image
#         else:
#             return image
#
#     @staticmethod
#     def get_seq(seq_index):
#         p = [0.5, 0.005, 0.2, 0.01, 360, 16, 5]
#         # e.g. Sometimes(0.5, GaussianBlur(0.3)) would blur roughly every second image.
#         sometimes = lambda aug: iaa.Sometimes(1.0, aug)  # p_1
#         seq_1 = iaa.Sequential(
#             [
#                 # @1 apply the following augmenters to most images
#                 iaa.Fliplr(p[0]),
#                 iaa.Flipud(p[0]),
#                 # @2 crop images by -5% to 10% of their height/width
#                 sometimes(iaa.CropAndPad(
#                     percent=(-p[1], p[1]),
#                     pad_mode='constant',
#                     pad_cval=(0, 0)
#                 )),
#                 # @3 Affine
#                 sometimes(iaa.Affine(
#                     scale={"x": (1 - p[2], 1 + p[2]), "y": (1 - p[2], 1 + p[2])},
#                     translate_percent={"x": (-p[3], p[3]), "y": (-p[3], p[3])},
#                     rotate=(0, p[4]),
#                     shear=(-p[5], p[5]),
#                     order=[0, 1],
#                     cval=(0, 0),
#                     mode='constant'
#                 )),
#                 # @4 execute 0 to 5 of the following (less important) augmenters per image
#                 iaa.SomeOf((0, p[6]),
#                     [
#                     iaa.Sharpen(alpha=(0, 0.1), lightness=(0.95, 1.05)),  # sharpen images
#                     iaa.Emboss(alpha=(0, 0.1), strength=(0, 1.0)),  # emboss images
#                     iaa.SimplexNoiseAlpha(iaa.OneOf([
#                         # search either for all edges or for directed edges,
#                         iaa.EdgeDetect(alpha=(0.5, 1.0)),
#                         # blend the result with the original image using a blobby mask
#                         iaa.DirectedEdgeDetect(alpha=(0.5, 1.0), direction=(0.0, 1.0)),
#                     ])),
#                     iaa.Invert(0.05, per_channel=True),  # invert color channels
#                     iaa.ContrastNormalization((0.5, 2.0), per_channel=0.5),  # improve or worsen the contrast
#                     sometimes(iaa.ElasticTransformation(alpha=(0.5, 3.5), sigma=0.25)),
#                     sometimes(iaa.PiecewiseAffine(scale=(0.01, 0.05))),  # sometimes move parts of the image around
#                     sometimes(iaa.PerspectiveTransform(scale=(0.01, 0.1)))
#                     ], random_order=True
#                 )
#             ], random_order=True
#         )
#         seq_2 = iaa.Sequential([
#             iaa.Fliplr(0.5),
#             iaa.Flipud(0.5),
#             iaa.Affine(rotate=(-180, 180)),
#             iaa.CropAndPad(
#                 percent=(-0.2, 0.2),
#                 pad_mode='constant',
#                 pad_cval=(0, 0)
#             )
#             ], random_order=False)
#
#         seq_0 = iaa.Sequential()
#         if seq_index == 1:
#             seq = seq_1
#         elif seq_index == 2:
#             seq = seq_2
#         else:
#             seq = seq_0
#         return seq
