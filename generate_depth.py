import os
import sys
import cv2
from PIL import Image
import numpy as np
from tqdm import tqdm
import torch
from torchvision.transforms import ToTensor

device = torch.device('cuda')
zoe = torch.hub.load("isl-org/ZoeDepth", "ZoeD_N", pretrained=True).to(device)
data_dir = sys.argv[1]

mask_dir = os.path.join(data_dir, 'masks')
background = None
for f in os.listdir(mask_dir):
    mask_path = os.path.join(mask_dir, f)
    mask = cv2.imread(mask_path, -1)
    if len(mask.shape) > 2:
        mask = mask[:, :, 2]
        mask[mask > 0] = 255
        cv2.imwrite(mask_path, mask)
    mask = mask // 255
    mask = 1 - mask
    if background is None:
        background = mask
    else:
        background = np.multiply(background, mask)
quit()
def pil_to_batched_tensor(img):
    return ToTensor()(img).unsqueeze(0)

rgb_dir = os.path.join(data_dir, 'rgb')
output_dir = os.path.join(data_dir, 'depth')
os.makedirs(output_dir, exist_ok=True)
base_depth = None
with torch.no_grad():
    for filename in tqdm(sorted(os.listdir(rgb_dir))):
        image_path = os.path.join(rgb_dir, filename)
        image = Image.open(image_path)
        X = pil_to_batched_tensor(image).to(device)
        predicted_depth = zoe.infer(X, pad_input=False).cpu().numpy().squeeze()
        pred = predicted_depth*500

        bg_pred = np.multiply(pred, background).flatten()
        bg_pred = bg_pred[bg_pred != 0]
        bg_depth = np.median(bg_pred)

        if base_depth is None:
            base_depth = bg_depth
        else:
            scale = bg_depth / base_depth
            pred = pred * scale
        pred = pred.astype(np.uint16)
        cv2.imwrite(image_path.replace('rgb', 'depth'), pred)
