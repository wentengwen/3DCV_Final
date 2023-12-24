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