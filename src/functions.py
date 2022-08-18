from platform import platform
import shutil
import face_recognition as rf
import cv2
from os import listdir
from os.path import join
import pickle
import pandas as pd
import numpy as np
import os
import platform
from config import *



def faceLocations(img, model='hog'):
    face_locations = rf.face_locations(img, model=model)
    return face_locations

def drawBox(img, labels, normal_color, unknown_color, name_color):
    face_locations = faceLocations(img)
    if len(face_locations) > 0 :
        i = 0
        for y1, x2, y2, x1 in face_locations:
            margin = int(THIKNESS/2)

            """ 1. Main recangle
                2. Text rectangle
                3. Text
            """
            if labels[i] == UNKNOWN_FACE :
                color = unknown_color
            else:
                color = normal_color

            cv2.rectangle(img, (x1, y1), (x2, y2), color=color, thickness=THIKNESS)
            cv2.rectangle(img, (x1-margin, y1-HEIGHT_FONT), (x2+margin, y1), color=color, thickness=-1)
            cv2.putText(img, labels[i], (x1, y1), FONT_STYLE, FONT_SCALE, name_color, FONT_THIKNESS, cv2.LINE_AA)
            i += 1

    return img


def encodeImageSet(path):
    dir = listdir(path)
    length = len(dir)

    items = [join(path, dir[i]) for i in range(length)]
    images = [cv2.imread(items[i]) for i in range(length)]

    encodings = []
    labels = dict()
    for i in range(length):
        encoded = rf.face_encodings(images[i])
        # The image should only have one picture
        assert len(encoded) == 1

        # Save encodings and associated labels
        encodings.append(encoded[0].tolist())
        labels[i] = dir[i].split(sep='.')[0]

        # Pickle encoding file
        with open(join(path, ENCODING_FILE_NAME), 'wb+') as file:
            pickle.dump(encodings, file, protocol=pickle.HIGHEST_PROTOCOL)

        with open(join(path, LABEL_FILE_NAME), 'wb+') as file:
            pickle.dump(labels, file, protocol=pickle.HIGHEST_PROTOCOL)
    

    return np.asarray(encodings), labels

def identification(img, encodings, labels_dict, normal_color, unknown_color, name_color):
    encoded_img = rf.face_encodings(img)

    labels = []
    for i in range(len(encoded_img)):
        res = rf.compare_faces(encodings, encoded_img[i])
        labels.append(decodeResult(res, labels_dict))
    
    image = drawBox(img, labels, normal_color, unknown_color, name_color)
    return image


def unpickleFiles(path=WORKSPACE):
    path_encodings = join(path, ENCODING_FILE_NAME)
    path_labels = join(path, LABEL_FILE_NAME)

    # It return encodings, labels
    encodings = np.asarray(pd.read_pickle(path_encodings))
    labels = pd.read_pickle(path_labels)
    return encodings, labels 

def decodeResult(result, labels):
    if result.count(True) != 0:
        return labels[result.index(True)]
    else:
        return UNKNOWN_FACE


def add_encoding(path_image, past_to=WORKSPACE):

    # Encode the image
    image = cv2.imread(path_image)
    encoded = list(rf.face_encodings(image))

    # Get its label
    img_label = path_image.split("/")[-1].split(".")[0] 

    # Unpickle encodings and labels
    encodings, labels = unpickleFiles(past_to)

    # Add the label and the encoding to the file
    encodings = list(encodings)
    encodings.append(encoded)
    encodings = np.asarray(encodings)
    labels[len(labels)] = img_label

    # Pickle the changements
    with open(join(past_to, ENCODING_FILE_NAME), 'wb+') as file:
        pickle.dump(encodings, file, protocol=pickle.HIGHEST_PROTOCOL)

    with open(join(past_to, LABEL_FILE_NAME), 'wb+') as file:
        pickle.dump(labels, file, protocol=pickle.HIGHEST_PROTOCOL)

    # Copy the image to the workspace

    os_name = platform.system()


    windows_command = 'copy "'+path_image.replace('/', '\\')+'" '+past_to
    linux_command = "cp "+path_image+" "+past_to

    if os_name == WINDOWS:
        command = windows_command
    elif os_name == LINUX:
        command = linux_command

    os.system(command)


def delete_encoding(index, path=WORKSPACE):
    encodings, labels = unpickleFiles(path)

    label_list = list(labels.values())
    path_image = os.path.join(WORKSPACE, label_list[index]+".jpg")

    os.remove(path_image)

    label_list.pop(index)
    encodings = list(encodings)
    encodings.pop(index)
    encodings = np.asarray(encodings)

    dictionary = {}
    for i in range(len(label_list)):
        dictionary[i] = label_list[i]
    

    # Pickle encoding file
    with open(join(path, ENCODING_FILE_NAME), 'wb+') as file:
        pickle.dump(encodings, file, protocol=pickle.HIGHEST_PROTOCOL)

    with open(join(path, LABEL_FILE_NAME), 'wb+') as file:
        pickle.dump(dictionary, file, protocol=pickle.HIGHEST_PROTOCOL)



# file = pd.read_pickle('images/train/encodings.pkl')
# labels = pd.read_pickle('images/train/labels.pkl')

# print(np.asarray(file).shape)
# print(np.asarray(labels))

# encodeImageSet('images/train')

# encodings, labels = unpickleFiles(WORKSPACE)
# print(labels, len(encodings))

# delete_encoding(2)
# encodings, labels = unpickleFiles(WORKSPACE)
# print(labels, len(encodings))
# path_image = "Billal Mokhtari"
# ind = path_image.index(" ")
# path_image = list(path_image)
# path_image.insert(ind, "\\")
# path_image = ''.join(path_image)
# print(path_image)
# img = cv2.imread('images/test/Paco De Lucia.jpg')

# image = identification(img, encodings, labels)
# cv2.imshow('image', image)
# cv2.waitKey(0)