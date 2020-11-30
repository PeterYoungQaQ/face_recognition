# 使用方法
# python pic_resize.py --shape-predictor shape_predictor_68_face_landmarks.dat --image images/example_01.jpg

from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import argparse
import imutils
import dlib
import cv2

# 运行程序的调用参数
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
                help="path to facial landmark predictor")
ap.add_argument("-i", "--image", required=True,
                help="path to input image")
args = vars(ap.parse_args())

# 初始化dlib库函数关于人脸识别的部分，然后进行创建
# 以下是关于脸部识别和脸部校正
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])
fa = FaceAligner(predictor, desiredFaceWidth=256)

# 读取照片、调整大小、进行灰度化处理
image = cv2.imread(args["image"])
image = imutils.resize(image, width=800)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 原始图像并进行灰度化处理

cv2.imshow("Input", image)
rects = detector(gray, 2)

# 循环进行人脸检测
for rect in rects:
    # 获得人脸位置，并且将其扣出来
    # 使用人脸检测功能
    (x, y, w, h) = rect_to_bb(rect)
    faceOrig = imutils.resize(image[y:y + h, x:x + w], width=256)
    faceAligned = fa.align(image, gray, rect)

    import uuid
    # 做一个uuid序号来分类
    f = str(uuid.uuid4())
    cv2.imwrite("num" + f + ".png", faceAligned)

    # 演示最终结果
    cv2.imshow("Original", faceOrig)
    cv2.imshow("Aligned", faceAligned)

    cv2.waitKey(0)
