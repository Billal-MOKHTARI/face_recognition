import cv2
import face_recognition as rf
import functions as func
from config import *


def main(width = 1200, height = 720, flip_cam = FLIP_CAM, camID = 0, normal_color = NORMAL_COLOR, unknown_color = UNKNOWN_COLOR, name_color = NAME_COLOR):
    
    # Get encodings.pkl and labels.pkl
    encodings, labels = func.unpickleFiles(WORKSPACE)

    # Load Camera
    cap = cv2.VideoCapture(camID)
    cap.set(3, width)
    cap.set(4, height)

    while True :
        ret, frame = cap.read()

        if flip_cam :
            frame = cv2.flip(frame, 1)

        frame = func.identification(frame, encodings, labels, normal_color, unknown_color, name_color)

        cv2.imshow('Face Recognition', frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

