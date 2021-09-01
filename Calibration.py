from __future__ import print_function
import cv2 as cv
import argparse
from Camera import *
max_value = 255
max_value_H = 360//2
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'
save = 0
save_name = 'Save Values'

def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv.setTrackbarPos(low_H_name, window_detection_name, low_H)
def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv.setTrackbarPos(high_H_name, window_detection_name, high_H)
def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv.setTrackbarPos(low_S_name, window_detection_name, low_S)
def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv.setTrackbarPos(high_S_name, window_detection_name, high_S)
def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv.setTrackbarPos(low_V_name, window_detection_name, low_V)
def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv.setTrackbarPos(high_V_name, window_detection_name, high_V)
def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv.setTrackbarPos(high_V_name, window_detection_name, high_V)

def on_save_trackbar(val):
    global save
    save = val
    cv.setTrackbarPos(save_name, window_detection_name, save)

def savevalues(namelow,namehigh):
    global low_H
    global low_S
    global low_V
    global high_H
    global high_S
    global high_V
    low = np.array([low_H,low_S,low_V])
    np.savetxt(namelow, low, fmt='%d')
    high = np.array([high_H,high_S,high_V])
    np.savetxt(namehigh, high, fmt='%d')


cv.namedWindow(window_capture_name)
cv.namedWindow(window_detection_name)
cv.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
cv.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)
cv.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
cv.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
cv.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
cv.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar)
cv.createTrackbar(save_name,window_detection_name,save,2,on_save_trackbar)

parser = argparse.ArgumentParser(description='A test program.')
parser.add_argument("--camera", help="Select the camera from: Web-Cam/Intel", default= "Web-Cam")

args = parser.parse_args()

cameraString = args.camera
camera = Camera(cameraString)

print('Save in 1 : will save the Right hand boundaries')
print('Save in 2 : will save the Left boundaries')
while True:
    
    #ret, frame = cap.read()
    ret,frame = camera.getFrame()
    if frame is None:
        break
    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
    
    
    cv.imshow(window_capture_name, frame)
    cv.imshow(window_detection_name, frame_threshold)

    if(save == 1):
        savevalues('lowRight','highRight')
    if(save == 2):
        savevalues('lowLeft','highLeft')
    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        break