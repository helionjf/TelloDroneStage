import time

from djitellopy import tello
import cv2
from pyzbar.pyzbar import decode
from time import sleep


class StockMaj():
    def __init__(self, me):
        self.tel = me
        self.img = None
        self.isFinish = False
        self.isStart = False
        self.file = open("data.txt", "a")
        self.move = [0, 0, 0, 0]
        self.barcodeNone = True
        self.lastCommand = None
        self.test = 0
        self.localtime = 0

    def detectCode(self):
        det = decode(self.img)
        if not det:
            self.test = time.localtime().tm_sec - self.localtime
            if self.test > 5 and self.isStart is True:
                self.move = [0, 0, 0, 0]
                self.isFinish = True
            self.barcodeNone = True
        for barcode in det:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(self.img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            tmp = barcodeData.split()
            self.localtime = time.localtime().tm_sec
            if self.isStart is False and barcodeData == "start" and self.barcodeNone is True:
                self.isStart = True
                self.move = [-25, 0, 0, 0]
                self.barcodeNone = False
            elif tmp[0] == "Box" and self.barcodeNone is True:
                if self.lastCommand is not None:
                    if self.lastCommand == "\n" + tmp[0] + " " + tmp[1] + " " + tmp[2] + " " + tmp[3]:
                        break
                    else:
                        self.lastCommand = "\n" + tmp[0] + " " + tmp[1] + " " + tmp[2] + " " + tmp[3]
                        self.file.write("\n" + tmp[0] + " " + tmp[1] + " " + tmp[2] + " " + tmp[3])
                else:
                    self.lastCommand = "\n" + tmp[0] + " " + tmp[1] + " " + tmp[2] + " " + tmp[3]
                    self.file.write("\n" + tmp[0] + " " + tmp[1] + " " + tmp[2] + " " + tmp[3])
                self.barcodeNone = False
            elif barcodeData == "up 50" and self.barcodeNone is True:
                self.move = [0, 0, 25, 0]
                self.barcodeNone = False
            elif barcodeData == "left" and self.barcodeNone is True:
                self.move = [25, 0, 0, 0]
                self.barcodeNone = False
            elif barcodeData == "right" and self.barcodeNone is True:
                self.move = [-25, 0, 0, 0]
                self.barcodeNone = False
            elif barcodeData == "stop" and self.barcodeNone is True:
                self.move = [0, 0, 0, 0]
                self.barcodeNone = False
                self.isFinish = True
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(self.img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    def initProg(self):
        tmp = 0
        if self.tel.get_battery() < 50:
            print("ERROR : Drone doesn't have enough battery")
            self.tel.end()
        self.localtime = time.localtime().tm_sec
        while not self.isFinish:
            self.img = self.tel.get_frame_read().frame
            self.img = cv2.resize(self.img, (1280, 720))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                self.isFinish = True
            self.detectCode()
            cv2.imshow("Search", self.img)
            self.tel.send_rc_control(self.move[0], self.move[1], self.move[2], self.move[3])
            if tmp == 0:
                self.tel.takeoff()
                tmp = 1
        self.tel.land()
        self.tel.streamoff()
        self.file.close()


if __name__ == '__main__':
    me = tello.Tello()
    me.connect()
    me.streamon()
    StockMaj(me).initProg()
