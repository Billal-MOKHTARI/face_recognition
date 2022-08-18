from types import CellType
import cv2
import os
# GUI default configurations
NORMAL_COLOR = (0, 255, 255)
UNKNOWN_COLOR = (0, 0, 255)
NAME_COLOR = (0, 0, 0)
WIDTH = 1200
HEIGHT = 720
FLIP_CAM = True
WINDOWS = 'Windows'
LINUX = 'Linux'

# Program configurations
WORKSPACE = os.path.join("..", "workspace")
ENCODING_FILE_NAME = 'encodings.pkl'
LABEL_FILE_NAME = 'labels.pkl'

THIKNESS = 2
FONT_STYLE = cv2.FONT_HERSHEY_COMPLEX
UNKNOWN_FACE = 'Unknown'
FONT_SCALE = 0.7
HEIGHT_FONT = int(FONT_SCALE*30)
FONT_THIKNESS = 1

ICONS_PATH = os.path.join("..", "assets", "icons")

# Style configuration
STYLE_QTAB_WIDGET_FACES = "background-color: #323232; color: #ffee00"
STYLE_QTAB_WIDGET_CONF = "background-color: #323232; color: white"

STYLE_CENTRAL_WIDGET = "background-color : #323232"
STYLE_PUSH_BUTTON = "font-size: 16px; border-radius : 12; height : 35px; background-color : qlineargradient(spread:pad, x1:0.136364, y1:0.568, x2:0.972, y2:0.272727, stop:0 rgba(0, 211, 230, 255), stop:1 rgba(62, 91, 210, 255)); color: black"
STYLE_SPIN_BOX = "font-size: 16px; border-radius : 12; height : 30px; border : 1px solid white; color : white"
STYLE_FLIP_CAMERA_LABEL = "font-size:16px"