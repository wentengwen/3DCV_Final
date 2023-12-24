# Enhancing Augmented Reality Experiences through BundleSDF 3D Reconstruction

## Environment
1. Build the docker image (this only needs to do once and can take some time). This may takes 4 hours to complete.
```bash
cd BundleSDF/docker
docker build --network host -t nvcr.io/nvidian/bundlesdf .
```
2. Start a docker container.
```bash
cd BundleSDF/docker && bash run_container.sh

# Inside docker container, compile the packages which are machine dependent
bash build.sh
# In our computer, we need to reinstall scipy to solve "version `GLIBCXX_3.4.29' not found" error
pip uninstall scipy
pip install scipy==1.9
```


## Data Preparation
We include five sets of data in the ```BundleSDF/data```: 
- **chair_full**
- **milk**
- **saber_v2**
- **chair_estimate**
- **whitebox_v2**

The structure of the each data folder should look like this:
```
root
  ├──rgb/    (PNG files)
  ├──depth/  (PNG files, stored in mm, uint16 format. Filename same as rgb)
  ├──masks/  (PNG files. Filename same as rgb. 0 is background. Else is foreground)
  └──cam_K.txt   (3x3 intrinsic matrix)
```

Each directory contains ```rgb/, depth/, masks/``` subdirectories, corresponding to the RGB frames of the video, uint16 depth maps, and object masks computed by XMem, respectively. And it also includes the camera intrinsics file ```cam_K.txt```. Note that the ```depth/``` in **chair_full**, **milk**, and **saber_v2** contains RGB-D depth recorded by a depth camera, while the ```depth/``` in **chair_estimate** and **whitebox_v2** is obtained from estimated depth.
### Custom data
If you want to do experiments on custom RGB/RGB-D video, you can run **unpack_video.py** to extract and resize the RGB frames of video, and rename the folder as ```rgb/```.
```bash
python unpack_video.py [path to RGB video] [path to output dir] [width] [height]
# Example: extract frames and resize to 256x192
python unpack_video.py ./BundleSDF/data/saber_v2/rgb.mp4 ./BundleSDF/data/saber_v2/rgb 256 192
```
For object masks, please refer to the XMem section below to get ```masks/```.

**Note that the frame's name and size in ```rgb/, depth/, masks/``` shound be the same.**
## Model Download
1. Download pretrained weights of the feature matching model.
```bash
bash download_loftr.sh
```


## How to Run
1. Run 3D reconstruction for RGBD video.
```bash
cd BundleSDF
python run_custom.py --mode run_video --video_dir [video_dir] --out_folder [output_dir] --use_segmenter 1 --use_gui 1 --debug_level 2 --stride [stride] --shorter_side [image_shorter_side_size] --num_frames [num_frames]
# Take chair_full data for example.
cd BundleSDF
python run_custom.py --mode run_video --video_dir ./data/chair_full --out_folder ./outputs/chair_full --use_segmenter 1 --use_gui 1 --debug_level 2 --stride 5 --shorter_side 192 --num_frames 1829
```
2. Run 3D reconstruction for RGB video.
```bash
python generate_depth.py [video_dir]
cd BundleSDF
python run_custom.py --mode run_video --video_dir [video_dir] --out_folder [output_dir] --use_segmenter 1 --use_gui 1 --debug_level 2 --stride [stride] --shorter_side [image_shorter_side_size] --num_frames [num_frames]
# Take whitebox_v2 data for example.
python generate_depth.py ./data/whitebox_v2
cd BundleSDF
python run_custom.py --mode run_video --video_dir ./data/whitebox_v2 --out_folder ./outputs/whitebox_v2 --use_segmenter 1 --use_gui 1 --debug_level 2 --stride 5 --shorter_side 192 --num_frames 540
```

If you wish to use XMem for segmentation to obtain object masks by yourself, please follow the steps below to build XMem and run the following. ****You dont need to install XMem if you use the existing ```masks/``` in each data directory.**
## XMem
## Environment
You need to create another environment to run XMem.

1.Install package
```bash
cd XMem
pip install -r requirements_demo.txt
```
## Model Download
1.Download XMem pretrained model.
```bash
bash download_XMem.sh
```
## How to Run
1. Run XMem GUI to generate segmentation mask.
```bash
cd XMem
python interactive_demo.py --video [path to the video] --num_objects 1 --mask_size [width of the mask]
# Take saber_v2 for example.
python interactive_demo.py --video ../BundleSDF/data/saber_v2/rgb.mp4 --num_object 1 --mask_size 192
```
Default width of the mask is 192. 

2. You can use the GUI to select the target mask in any frame and generate masks for the entire video segment.

3. Since output is in the ```XMem/workspace/RGB/masks/```, and it needs to be manually moved to data root directory.
4. Convert the masks into grayscale and resize them using **mask_convert.py**.
```bash
python mask_convert.py [path to RGB masks dir] [path to output dir] [width] [height]
# Example: convert to 256x192 grayscale masks
python mask_convert.py ./BundleSDF/data/saber_v2/mask_vis ./BundleSDF/data/saber_v2/masks 256 192
```
