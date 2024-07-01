from djitellopy import tello
import cv2
import ReadKeyboard as rk
from time import sleep
import numpy as np

main_win = np.zeros((370, 450, 3), dtype=np.uint8)

global droneSpeedfb, droneYaw, dronelr1

drone = tello.Tello()

drone.connect()
sleep(5)
print(drone.get_battery())
drone.streamon()


def faceDetection(img):
    cascade = cv2.CascadeClassifier("model/haarcascade_frontalface_default.xml")
    GrayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(GrayImg, 1.1, 8)

    faceList = []
    faceAreaList = []

    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (176,129,35), 2)
        centerX = x + w //2
        centerY = y + h //2
        area = w*h
        cv2.circle(img, (centerX,centerY), 2, (241,190,105), 2)
        cv2.line(img, (centerX,0), (centerX, 240), (130,70,130), 1)
        cv2.line(img, (0, centerY), (320, centerY), (80, 170, 30), 1)
        faceList.append([centerX,centerY])
        faceAreaList.append(area)

    if len(faceAreaList) != 0:
        i = faceAreaList.index(max(faceAreaList))
        return img, [faceList[i], faceAreaList[i]]
    else:
        return img, [[0,0], 0]

def faceTracking(data):
    area = data[1]
    x,y = data[0]
    if area != 0:
        if area > 10500:
            droneSpeedfb = -20
        elif area < 6000:
            droneSpeedfb = 20
        elif area < 10500 and area > 6000:
            droneSpeedfb = 0

        wdiff = x - 160

        if wdiff > -20 and wdiff < 20:
            droneYaw = 0

        elif wdiff > 30:
            droneYaw = 30

        elif wdiff < -30:
            droneYaw = -30

        else:
            droneYaw = int(wdiff)


    else:
        droneYaw = 0
        droneSpeedfb = 0

    return droneSpeedfb, droneYaw


def getKeyPress():
    ud = 0
    if rk.KeyRead("UP"): drone.send_rc_control(0,0,30,0)
    elif rk.KeyRead("DOWN"): drone.send_rc_control(0,0,-30,0)

    if rk.KeyRead("l"):drone.land()
    if rk.KeyRead("t"):
        drone.takeoff()
        sleep(2)
        drone.send_rc_control(0,0,40,0)
        sleep(3)
        drone.send_rc_control(0,0,0,0)
        sleep(1)

    return ud

while 1:
    img = drone.get_frame_read().frame
    img = cv2.resize(img,(720,480))
    img1 = img

    img, data = faceDetection(img)
    getKeyPress()
    fb, y = faceTracking(data)


    drone.send_rc_control(0,fb,0,y)

    cv2.imshow("Image", img)
    cv2.waitKey(1)



