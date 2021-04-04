import cv2
from pyzbar.pyzbar import decode
from djitellopy import tello
from time import sleep

me = tello.Tello()

me.connect()
me.streamon()
me.takeoff()


def demo1(me):
    me.set_speed(60)
    sleep(1)
    me.rotate_clockwise(360)
    sleep(7)
    me.rotate_counter_clockwise(360)
    sleep(7)
    me.move_up(50)
    sleep(2.2)
    me.move_down(100)
    sleep(3.5)
    me.move_up(50)
    sleep(2.2)
    me.flip_right()
    sleep(4)
    me.flip_left()
    sleep(4)
    me.land()
    me.streamoff()
    sleep(2)
    me.end()
    exit(1)


def detectQrCode(img, me):
    det = decode(img)

    for barcode in det:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        if barcodeData == "demo1":
            demo1(me)
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


while True:
    img = me.get_frame_read().frame
    img = cv2.resize(img, (720, 480))
    detectQrCode(img, me)
    cv2.imshow("QRCode Scanner", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        me.streamoff()
        break

cv2.destroyAllWindow()
