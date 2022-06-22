# FAS_Datamager
This repo can be used to manage publicly available datasets for the face anti-spoofing problem.



# News
2022-06-20: Upload the code. Still in development period. More to be Completed.


# Dataset introduction
Below are the information about the public face anti-spoofing datasets. In the 'Attack Types' column, 'P' means printed photo/paper photo attack,
'R' means replay attack (screen display attack), 'M' means 3D mask attack, 'PM' means paper mask attack.
(The modalities in each data is to be completed)


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

# Usage
## Set up environments
```sh
# requirements
pip install -r requirements.txt

# opencv 
conda install -c conda-forge opencv

# pytorch/torchvision 
conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch

# We use mtcnn (mxnet version) for face detection
git clone https://github.com/YYuanAnyVision/mxnet_mtcnn_face_detection.git
pip install mxnet # cpu version is fine
```

## Manage video datasets
Some datasets are released with the raw videos, such as NTU ROSE-YOUTU, CASIA-FASD, etc. 
We can extract the frames and save the frames as images (.png). 
```sh
export PYTHONPATH=.
python preliminary/extract_frame_from_video --dataset <Dataset_Name> --root_dir <the directory where you put the original dataset> --save_dir --root_dir <the directory where you save the processed dataset>
```
After the extraction, the processed files would have the same folder structure as the raw videos.  
## Manage hdf5 datasets
Some datasets are released with the processed files in the HDF5 format, such as the 3DMAD, CSMAD, and WMCA datasets. 
The authors told that the raw data is too large to share and thus they process the data (e.g. cropping faces) and store the data in the HDF5 format for release.
After downloading the datasets (3DMAD, CSMAD, and WMCA dataset), we can use the methods in [datasets/hdf5_datasets.py](datasets/hdf5_datasets.py) to load the data.




