import face_recognition
from PIL import Image


def demo_one():
    image = face_recognition.load_image_file("../test_pic/12.jpg")
    face_locations = face_recognition.face_locations(image)
    print(f"一共识别出{len(face_locations)}张人脸")

    for face_location in face_locations:
        top, right, bottom, left = face_location
        print(f"人脸的位置：{top}，{bottom}，{left}，{right}")
        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        pil_image.show()
        pil_image.save(f"new{face_location}.png")


demo_one()
