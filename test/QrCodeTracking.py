import cv2
from pyzbar.pyzbar import decode
from djitellopy import tello
from demo1 import demo1
from demo2 import demo2

# init drone state

me = tello.Tello()
me.connect()
me.streamon()
me.takeoff()

# permet de detecter un qrcode dans une image, si le qrcode est demo1 ou demo2 cela lancera les demos differentes


def detectQrCode(img, me):
    det = decode(img)

    for barcode in det:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        if barcodeData == "demo1":
            demo1(me)
        elif barcodeData == "demo2":
            demo2(me)
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


# main loop pour detecter un qrcode

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
