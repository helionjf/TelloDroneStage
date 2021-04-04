import cv2
import numpy as np
from djitellopy import tello
from pyzbar.pyzbar import decode
import time

me = tello.Tello()
me.connect()
print(me.get_battery())

me.streamon()
time.sleep(2.2)
me.takeoff()
time.sleep(2.2)
me.send_rc_control(0, 0, 25, 0)
time.sleep(2.2)

w, h = 360, 240
FbRange = [6200, 6800]
pid = [0.4, 0.4, 0]  # PID = proportionnel, integral, derivé
pError = 0


def findFace(img):
    cv2.circle(img, (int(360 / 2), int(240 / 2)), 10, (0, 255, 0))
    det = decode(img)

    myFaceListC = []
    myFaceListArea = []

    for barcode in det:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(img, (x, y), (x + w, y + w), (0, 0, 255), 2)
        cx = x + int(h / 2)
        cy = y + int(w / 2)
        area = w * h
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]


def trackFace(me, info, w, pid, pError):
    area = info[1]
    x, y = info[0]
    fb = 0

    error = x - w // 2
    speed = (pid[0] * error) + (pid[1] * (error - pError))
    print("oui", speed)
    speed = int(np.clip(speed, -100, 100))
    print("non", speed)
    if FbRange[0] < area < FbRange[1]:
       fb = 0
    if area > FbRange[1]:
       fb = -20
    elif area < FbRange[0] and area != 0:
       fb = 20
    if x == 0:
       speed = 0
       error = 0

    me.send_rc_control(0, fb, 0, speed)
    return error


while True:
    img = me.get_frame_read().frame
    img = cv2.resize(img, (w, h))
    img, info = findFace(img)
    trackFace(me, info, w, pid, pError)
    cv2.putText(img, f'[{info[0][0]}, {info[0][1]}, {info[1]}]', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("Facetracking", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        me.streamoff()
        me.end()
        break
