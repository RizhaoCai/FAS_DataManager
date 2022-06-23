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
python preliminary/extract_frame_from_video.py --dataset <Dataset_Name> --root_dir <the directory where you put the original dataset> --save_dir --root_dir <the directory where you save the processed dataset>
```
After the extraction, the processed files would have the same folder structure as the raw videos.  
## Manage hdf5 datasets
Some datasets are released with the processed files in the HDF5 format, such as the 3DMAD, CSMAD, and WMCA datasets. 
The authors told that the raw data is too large to share and thus they process the data (e.g. cropping faces) and store the data in the HDF5 format for release.
After downloading the datasets (3DMAD, CSMAD, and WMCA dataset), we can use the methods in [datasets/hdf5_dataset.py](datasets/hdf5_dataset.py) to load the data.

# Generate data list
We can use a data list file to indicate what images or frames we want to load for training or testing.
The data list in the below csv format: 
```csv
examples/1.png,0
```
The first column indicates the path of the image/frame, and the second column indicate image's label. 
The label format is that '0' means a genuine face/real face, '1' means a printed paper/photo attack, '2' means a replay/screen attack, and '3' means a mask attack.
For a binary classification network, the labels can be transformed as binary: 0 for real and 1 for fake. 

Please check [preliminary/generate_data_list.py](preliminary/generate_data_list.py) to see how to generate data list files for different datasets.
For example, to generate a data list for the NTU ROSE-YOUTU dataset, you may refer to the below code snippet

```python
from preliminary.generate_data_list import write_protocol_list_file
write_protocol_list_file(base_dir='/home/rizhao/data/FAS/frames/ROSE-YOUTU', subset_name="ROSE-TRAIN",
                          regx=r"(.+)/ROSE-YOUTU/(train)/(.+)\.png")
write_protocol_list_file(base_dir='/home/rizhao/data/FAS/frames/ROSE-YOUTU', subset_name="ROSE-TEST",
                          regx=r"(.+)/ROSE-YOUTU/(test)/(.+)\.png")
```
Also, you can also use the below shell script to do the batch processing 
```sh
python -c "from preliminary.generate_data_list import write_protocol_list_file;\
write_protocol_list_file(base_dir='/home/rizhao/data/FAS/frames/ROSE-YOUTU', subset_name='ROSE-TRAIN', regx=r'(.+)/ROSE-YOUTU/(train)/(.+)\.png')"
```
# Get a dataset instance with a data list
The file [get_dataset.py](get_dataset.py) implements the functions for getting a dataset instance with a data list.
You can run an example with the below command.
```sh
python get_dataset.py
```


