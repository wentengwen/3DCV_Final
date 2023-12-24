import cv2
import os
import sys

def main(*args):
    rgb_folder_path = sys.argv[1]
    gray_folder_path = sys.argv[2]
    h, w = int(sys.argv[4]), int(sys.argv[3])
    
    os.makedirs(gray_folder_path, exist_ok=True)

    for filename in os.listdir(rgb_folder_path):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            rgb_image_path = os.path.join(rgb_folder_path, filename)
            img_rgb = cv2.imread(rgb_image_path)

            img_rgb_resized = cv2.resize(img_rgb, (w, h))
            
            img_gray = cv2.cvtColor(img_rgb_resized, cv2.COLOR_BGR2GRAY)
            
            img_gray[img_gray != 0] = 255
            
            base_filename = os.path.splitext(filename)[0]
            
            non_zero_digits = str(int(base_filename))
            formatted_filename = non_zero_digits.zfill(6) + '.png'
            
            gray_image_path = os.path.join(gray_folder_path, formatted_filename)

            cv2.imwrite(gray_image_path, img_gray)

    print('convert all masks into grayscale, saving to:', gray_folder_path)

if __name__ == '__main__':
    main()