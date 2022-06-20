# FAS_Datamager
This repo can be used to manage publicly available datasets for the face anti-spoofing problem.



# News
2022-06-20: Upload the code. Still in development period. More to be Completed.

# Prerequisites
```sh
# requirements
pip install -r requirements.txt
# opencv 
conda install -c conda-forge opencv
# pytorch/torchvision 
conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
# 
# mtcnn
# mxnet + mtcnn (https://github.com/YYuanAnyVision/mxnet_mtcnn_face_detection.git)
git clone https://github.com/YYuanAnyVision/mxnet_mtcnn_face_detection.git
pip install mxnet # cpu version is fine
```

# Dataset introduction
According to how the dataset are released and organized here are how these dataset organized


|  Dataset name   | Attack types| Release format| Release with raw images or videos |
|  ----  | ----  |   ----  | ----  |
| CASIA-MFSD (CASIA-FASD)  | P, R | Video  | Yes  | 
| IDIAP ReplayAttack  |  P,R | Video | Yes  |
| NTU ROSE-YOUTU   |  P, R, PM | Video | Yes  |
| SiW   | P, R, PM | Video | Yes  |
| MSU MFSD|   P, R | Video  | Yes  |
| OULU-NPU |   P, R  | Video  | Yes  |
| WMCA |   P, R, M  | HDF5  | No |
| HQ-WMCA |   P, R, M  | HDF5  | No  |
| CASIA-SURF |   P, R, M  | HDF5  | No|
| CASIA-SURF-3DMask |   P, R, M  | HDF5  | No|
|CASIA-SURF HIFI_MASK| M|Image|No|
| WFFD |  P  | Image  | Yes|
| CeFA |  P,R,M  | Image  | Yes|
| PADAISI |  P,R,M  | Image  | Yes|
|HKBU_MAR V2|M |Video | Yes|
|CelebA-Spoof|P|Image|Yes|

# Dataset format
(TODO)
In terms of the label, 0,1,2,3 mean genuine face, photo attack, video attack, and mask attack, respectively.
A video, an image, or a folder would be regarded as a unit.
# Usage
(TODO)

