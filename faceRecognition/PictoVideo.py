import os
import cv2
import numpy as np

folder_name = 'dataset/save_pic/'
image_extension = '.jpg'
output_video_name = 'output'
output_video_extension = '.avi'
frame_per_second = 2

images = []

for frame in range(0, 1500, 25):
    images.append(str(frame) + image_extension)

frame = cv2.imread(os.path.join(folder_name, images[1]))
height, width, layers = frame.shape
size = (width, height)

out = cv2.VideoWriter(output_video_name + output_video_extension, 0, frame_per_second, size)

for image in images:
    out.write(cv2.imread(os.path.join(folder_name, image)))

cv2.destroyAllWindows()
out.release()
