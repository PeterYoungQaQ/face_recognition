from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import cv2
from scipy import misc
import tensorflow as tf
import numpy as np
import os
from utils import file_processing, image_processing
import face_recognition

resize_width = 160
resize_height = 160


def face_recognition_image(model_path, dataset_path, filename, image_path, i):
    # 加载数据库的数据
    dataset_emb, names_list = load_dataset(dataset_path, filename)
    # 初始化mtcnn人脸检测
    face_detect = face_recognition.Facedetection()
    # 初始化facenet
    face_net = face_recognition.facenetEmbedding(model_path)

    image = image_processing.read_image_gbk(image_path)
    # 获取 判断标识 bounding_box crop_image
    bboxes, landmarks = face_detect.detect_face(image)
    bboxes, landmarks = face_detect.get_square_bboxes(bboxes, landmarks, fixed="height")
    if bboxes == [] or landmarks == []:
        print("-----no face")
        cv2.imwrite("./dataset/save_pic/" + str(i) + ".jpg", image)
    else:
        print("-----image have {} faces".format(len(bboxes)))
        face_images = image_processing.get_bboxes_image(image, bboxes, resize_height, resize_width)
        face_images = image_processing.get_prewhiten_images(face_images)
        pred_emb = face_net.get_embedding(face_images)
        pred_name, pred_score = compare_embadding(pred_emb, dataset_emb, names_list)
        # 在图像上绘制人脸边框和识别的结果
        show_info = [n + ':' + str(s)[:5] for n, s in zip(pred_name, pred_score)]
        # image_processing.show_image_bboxes_text("face_recognition", image, bboxes, show_info, i)
        bgr_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        for name, box in zip(show_info, bboxes):
            box = [int(b) for b in box]
            cv2.rectangle(bgr_image, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2, 8, 0)
            cv2.putText(bgr_image, name, (box[0], box[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), thickness=2)
        # cv2.imshow(title, bgr_image)
        # cv2.waitKey(0)
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        cv2.imwrite("./dataset/save_pic/" + str(i) + ".jpg", rgb_image)


def load_dataset(dataset_path, filename):
    '''
    加载人脸数据库
    :param dataset_path: embedding.npy文件（faceEmbedding.npy）
    :param filename: labels文件路径路径（name.txt）
    :return:
    '''
    embeddings = np.load(dataset_path)
    names_list = file_processing.read_data(filename, split=None, convertNum=False)
    return embeddings, names_list


def compare_embadding(pred_emb, dataset_emb, names_list, threshold=0.65):
    # 为bounding_box 匹配标签
    pred_num = len(pred_emb)
    dataset_num = len(dataset_emb)
    pred_name = []
    pred_score = []
    for i in range(pred_num):
        dist_list = []
        for j in range(dataset_num):
            dist = np.sqrt(np.sum(np.square(np.subtract(pred_emb[i, :], dataset_emb[j, :]))))
            dist_list.append(dist)
        min_value = min(dist_list)
        pred_score.append(min_value)
        if (min_value > threshold):
            pred_name.append('unknow')
        else:
            pred_name.append(names_list[dist_list.index(min_value)])
    return pred_name, pred_score


if __name__ == '__main__':
    model_path = 'models/20180408-102900'
    dataset_path = 'dataset/emb/faceEmbedding.npy'
    filename = 'dataset/emb/name.txt'
    for i in range(0, 1500, 25):
        image_path = 'dataset/test_pic/' + str(i) + '.jpg'
        face_recognition_image(model_path, dataset_path, filename, image_path, i)
