import cv2
import numpy as np
from djitellopy import tello
from pyzbar.pyzbar import decode
import time

# init drone state

me = tello.Tello()
me.connect()
print(me.get_battery())

me.streamon()
time.sleep(2.2)
me.takeoff()

w, h = 360, 240
FbRange = [6200, 6800]
pid = [0.4, 0.4, 0]  # PID = proportionnel, integral, derivé
pError = 0


# permet de reconnaitre une cible à partir d'une image

def findFace(img):
    cv2.circle(img, (int(360 / 2), int(240 / 2)), 10, (0, 255, 0))
    # faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    # imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)
    det = decode(img)

    myFaceListC = []
    myFaceListArea = []

    for barcode in det:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(img, (x, y), (x + w, y + w), (0, 0, 255), 2)
        cx = x + int(w / 2)
        cy = y + int(h / 2)
        area = w * h
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]


# permet de ce deplacer vers la cible reconnue

def trackFace(me, info, w, pid, pError):
    area = info[1]
    x, y = info[0]
    fb = 0

    error = x - w // 2
    speed = (pid[0] * error) + (pid[1] * (error - pError))
    speed = int(np.clip(speed, -100, 100))
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


# main loop permettant, à chaque frame, de detecter une cible puis ce deplacer vers elle

while True:
    img = me.get_frame_read().frame
    img = cv2.resize(img, (w, h))
    img, info = findFace(img)
    pError = trackFace(me, info, w, pid, pError)
    cv2.putText(img, f'[{info[0][0]}, {info[0][1]}, {info[1]}]', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("Face Tracking", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        me.streamoff()
        me.end()
        cv2.destroyAllWindows()
        break
