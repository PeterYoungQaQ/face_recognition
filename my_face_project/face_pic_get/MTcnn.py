# -*- coding: utf-8 -*-
import cv2
from mtcnn.mtcnn import MTCNN

detector = MTCNN()

video_capture = cv2.VideoCapture("../test_video/weibo.mp4")
c = 0
video_name = "weibo"
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    timeF = 25
    if c % timeF == 0:  # save as jpg every 20 frame
        result = detector.detect_faces(frame)
        for i in range(len(result)):
            bounding_box = result[i]['box']
            # cv2.rectangle(frame, (bounding_box[0], bounding_box[1]), (bounding_box[0] + bounding_box[2],
            # bounding_box[1] + bounding_box[3]), (0, 155, 255),2)
            crop = frame[bounding_box[1]:bounding_box[1] + bounding_box[3],
                   bounding_box[0]:bounding_box[0] + bounding_box[2]]

            # 人脸匹配

            cv2.imwrite('../save_pic/' + video_name + '/' + str(c) + '_' + str(i) + '.jpg', crop)  # save as jpg
        cv2.imwrite('../save_pic/' + video_name + '/' + str(c) + ".jpg", frame)
    c += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
