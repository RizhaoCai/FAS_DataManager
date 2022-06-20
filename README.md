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


|  Dataset name   | Attack types| Release format| Released with raw images or videos |
|  ----  | ----  |   ----  | ----  |
| CASIA-MFSD (CASIA-FASD)  | P, R | Video (.avi) | Yes  | 
| IDIAP ReplayAttack  |  P,R | Video (.avi) | Yes  |
| NTU ROSE-YOUTU   |  P, R, PM | Video (.mp4) | Yes  |
| SiW   | P, R, PM | Video (.mov) | Yes  |
| MSU MFSD|   P, R | Video (.mp4)  | Yes  |
| OULU-NPU |   P, R  | Video (.avi)  | Yes  |
| WMCA |   P, R, M  | HDF5  | No |
| HQ-WMCA |   P, R, M  | HDF5  | No  |
| CASIA-SURF |   P | Image (.jpg)  | No|
| CASIA-SURF-3DMask |   P, R, M  | Video (.MOV)  | No|
|CASIA-SURF HIFI_MASK| M|Image|No|
| WFFD |  P  | Image (.jpg)  | Yes|
| CeFA |  P,R,M  | Image (.jpg) | Yes|
| PADAISI |  P,R,M  | Image (.jpg)   | Yes|
|HKBU_MAR V2|M |Video (.avi) | Yes|
|CelebA-Spoof|P|Image (.png)|Yes|

# Dataset format
(TODO)
In terms of the label, 0,1,2,3 mean genuine face, photo attack, video attack, and mask attack, respectively.
A video, an image, or a folder would be regarded as a unit.
# Usage
(TODO)

