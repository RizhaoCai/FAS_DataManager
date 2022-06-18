# FAS_Datamager
This is a tool set for managing 

# Prerequisites
```
# opencv 
conda install -c conda-forge opencv
# pytorch/torchvision 
conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
# 
# mtcnn
# dlib
# yaml
# mxnet + mtcnn (https://github.com/YYuanAnyVision/mxnet_mtcnn_face_detection.git)
git clone https://github.com/YYuanAnyVision/mxnet_mtcnn_face_detection.git
```

# Dataset introduction
According to how the dataset are released and organized here are how these dataset organized


|  Dataset name   | Attack types| Release format| Release with raw |
|  ----  | ----  |   ----  | ----  |
| CASIA-MFSD  | P, R | videos  | Yes  | 
| IDIAP ReplayAttack  |  P,R | videos | Yes  |
| NTU ROSE-YOUTU   |  P, R, PM | videos | Yes  |
| SiW   | P, R, PM | videos | Yes  |
| MSU MFSD   P, R, PM | videos  | Yes  |
| OULU-NPU |   P, R  | videos  | Yes  |
| WMCA |   P, R, M  | HDF5  | No |
| HQ-WMCA |   P, R, M  | HDF5  | No  |
| CASIA-SURF |   P, R, M  | HDF5  | No|
| CASIA-SURF-3DMask |   P, R, M  | HDF5  |
| WFFD |    |   |
| CeFA |    | Image  | Yes|
| PADAISI |    | images  | Yes|
|HKBU_MAR V2|M |Video | Yes|
|HIFI_MASK| M|Images|No|
|CelebA-Spoof|P|images|Yes|

# Dataset format
A data list file is in the csv format.
```csv
# file path, label
xxx.avi.zip, 0
```
In terms of the label, 0,1,2,3 mean genuine face, photo attack, video attack, and mask attack, respectively.
A video, an image, or a folder would be regarded as a unit.
# Usage
1. export PYTHONPATH=.
# Ackowledgement
The management method of using zip files is inspired by Dr. Sun Wenyun.