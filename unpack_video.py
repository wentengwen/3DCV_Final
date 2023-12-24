import cv2
import os
import sys

def main(*args):
    input_video = sys.argv[1]
    output_folder = sys.argv[2]
    h, w = int(sys.argv[4]), int(sys.argv[3])
    
    target_size = (w, h)
        
    os.makedirs(output_folder, exist_ok=True)

    cap = cv2.VideoCapture(input_video)

    frame_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break
        
        resized_frame = cv2.resize(frame, target_size)
        
        output_filename = os.path.join(output_folder, f'{frame_count:06d}.png')
        cv2.imwrite(output_filename, resized_frame)

        frame_count += 1

    cap.release()

    print(f'Extract {frame_count} frames，save in {output_folder}.')


if __name__ == '__main__':
    main()