from djitellopy import tello
import time
import ReadKeyPress as rk
import cv2
import os

drone = tello.Tello()
drone.connect()

drone.streamon()
global dronefeed

dir= 'C:/Users/dhupa/OneDrive/Desktop/drone/facerecoginazation'
os.chdir(dir)

def faceDetection(img):
    model = cv2.CascadeClassifier("model/haarcascade_frontalface_default.xml")
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = model.detectMultiScale(grayImg, 1.1, 8)
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y),(x+w, y+h), (100,129,35), 3)
    return img

def Teleoperation():
    LeftRight, ForwardBackward, UpDown, yaw = 0,0,0,0

    if rk.KeyRead("LEFT"):
        LeftRight = -50
    elif rk.KeyRead("RIGHT"):
        LeftRight = 50
    elif rk.KeyRead("UP"):
        ForwardBackward = 50
    elif rk.KeyRead("DOWN"):
        ForwardBackward = -50
    elif rk.KeyRead("u"):
        UpDown = 50
    elif rk.KeyRead("d"):
        UpDown = -50
    elif rk.KeyRead("t"):
        drone.takeoff()
        time.sleep(5)
    elif rk.KeyRead("l"):
        drone.land()
    elif rk.KeyRead("a"):
        yaw = -30
    elif rk.KeyRead("c"):
        yaw = 30
    elif rk.KeyRead("s"):
        cv2.imwrite(f'{time.time()}.jpg', dronefeed)
        time.sleep(0.2)

    return [LeftRight, ForwardBackward, UpDown, yaw]

while True:
    rc_data = Teleoperation()
    drone.send_rc_control(rc_data[0], rc_data[1], rc_data[2], rc_data[3])
    time.sleep(0.05)
    dronefeed = drone.get_frame_read().frame
    dronefeed = cv2.resize(dronefeed, (360,240))
    processedImg = faceDetection(dronefeed)
    cv2.imshow("Surveillance Video", processedImg)
    cv2.waitKey(1)