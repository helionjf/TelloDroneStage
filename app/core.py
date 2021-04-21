from kivy.app import App
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.properties import BooleanProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from djitellopy import tello
from pyzbar.pyzbar import decode
import numpy as np
import math
import cv2
import threading
import ffmpeg


class CustomDropDown(DropDown):
    isShowFlipButton = BooleanProperty(False)
    isFaceTracking = BooleanProperty(False)
    isQrCodeAction = BooleanProperty(False)
    isQrCodeTracking = BooleanProperty(False)
    isCircleMod = BooleanProperty(False)
    isRoundMod = BooleanProperty(False)
    isReboundMod = BooleanProperty(False)
    isBigAngle = BooleanProperty(False)


def circle(radius: int, direction: str, rotation: str, inclinaison: int, speed: int,
           tello):
    """ Dessine un cercle avec pour point point de départ et d'arrivée la position actuelle
        :param radius: distance entre le drone et le centre du cercle qu'il va dessiner
        :param direction: indique s'il part en avant ou en arrières par rapport à son point de départ (avant/arriere)
        :param rotation: sens de la rotation (cw/ccw)
        :param inclinaison: inclinaison du cercle en degrès (de -90 à 90) par raport au sol (0 degrès)
    """

    assert radius > 50, "Le rayon du cercle doit être supérieur à 50 cm"
    assert -90 <= inclinaison <= 90, "L'inclinaison doit être comprise entre -90 et 90"

    z = math.cos(inclinaison / 90) * radius
    if inclinaison < 0:
        z *= -1
    if direction == 'avant':
        if rotation == 'cw':
            tello.curve_xyz_speed(x1=radius, y1=radius, z1=int(z), x2=2 * radius, y2=0, z2=0, speed=speed)
            tello.curve_xyz_speed(x1=-radius, y1=-radius, z1=int(-z), x2=-2 * radius, y2=0, z2=0, speed=speed)
        if rotation == 'ccw':
            tello.curve_xyz_speed(x1=radius, y1=-radius, z1=int(z), x2=2 * radius, y2=0, z2=0, speed=speed)
            tello.curve_xyz_speed(x1=-radius, y1=radius, z1=int(-z), x2=-2 * radius, y2=0, z2=0, speed=speed)
    if direction == 'arriere':
        if rotation == 'cw':
            tello.curve_xyz_speed(x1=-radius, y1=-radius, z1=int(z), x2=-2 * radius, y2=0, z2=0, speed=speed)
            tello.curve_xyz_speed(x1=radius, y1=radius, z1=int(-z), x2=2 * radius, y2=0, z2=0, speed=speed)
        if rotation == 'ccw':
            tello.curve_xyz_speed(x1=-radius, y1=radius, z1=int(z), x2=-2 * radius, y2=0, z2=0, speed=speed)
            tello.curve_xyz_speed(x1=radius, y1=-radius, z1=int(-z), x2=2 * radius, y2=0, z2=0, speed=speed)


# Kivy Camera permet d'afficher la camera ainsi que de gerer les bouttons
class KivyCamera(Image):

    def __init__(self, capture, fps, **kwargs):
        self.dropdown = CustomDropDown()
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        self.forward = None
        self.backward = None
        self.left = None
        self.Right = None
        self.up = None
        self.down = None
        self.rotateR = None
        self.rotateL = None
        self.flip_thread = None
        self.FbRange = [6200, 6800]
        self.pid = [0.4, 0.4, 0]
        self.pError = 0
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down, on_key_up=self._on_keyboard_up)
        self.mainbutton = Button(text='Menu', size=(150, 50), pos=(650, 550))
        self.add_widget(self.mainbutton)
        self.mainbutton.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))
        Clock.schedule_interval(self.update, 1.0 / fps)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down, on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'up':
            self.on_move_forward()
        elif keycode[1] == 'down':
            self.on_move_backward()
        elif keycode[1] == 'left':
            self.on_move_left()
        elif keycode[1] == 'right':
            self.on_move_right()
        elif keycode[1] == 'z':
            self.on_move_up()
        elif keycode[1] == 's':
            self.on_move_down()
        elif keycode[1] == 'q':
            self.on_move_rotateL()
        elif keycode[1] == 'd':
            self.on_move_rotateR()
        elif keycode[1] == 'a':
            self.takeoff()
        elif keycode[1] == 'e':
            self.land()
        return True

    def _on_keyboard_up(self, keyboard, keycode):
        if keycode[1] == 'up':
            self.off_move_forward()
        elif keycode[1] == 'down':
            self.off_move_backward()
        elif keycode[1] == 'left':
            self.off_move_left()
        elif keycode[1] == 'right':
            self.off_move_right()
        elif keycode[1] == 'z':
            self.off_move_up()
        elif keycode[1] == 's':
            self.off_move_down()
        elif keycode[1] == 'q':
            self.off_move_rotateL()
        elif keycode[1] == 'd':
            self.off_move_rotateR()
        return True

    def update(self, dt):
        frame = self.capture.get_frame_read().frame
        if self.dropdown.isFaceTracking:
            frame, info = self.findFace(frame)
            self.pError = self.trackFace(self.capture, info, self.width, self.pid, self.pError)
        if self.dropdown.isQrCodeTracking:
            frame, info = self.findQrCode(frame)
            self.pError = self.trackFace(self.capture, info, self.width, self.pid, self.pError)
        if self.dropdown.isQrCodeAction:
            self.detectQrCode(frame)
        if self.dropdown.isRoundMod:
            h = threading.Thread(name='360', target=self.round)
            h.start()
            self.dropdown.isRoundMod = False
        if self.dropdown.isReboundMod:
            h = threading.Thread(name='rebound', target=self.rebound)
            h.start()
            self.dropdown.isReboundMod = False
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tobytes()
        image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = image_texture
        self.ids.battery_label.text = "Battery: " + str(self.capture.get_battery()) + "%"
        self.ids.temperature_label.text = "Temperature: " + str(self.capture.get_temperature()) + "°C"
        self.ids.barometer_label.text = "Altitude: " + str(self.capture.get_height()) + "cm"
        self.ids.time_flight_label.text = "Flight Time: " + str(self.capture.get_flight_time()) + "s"
        if self.dropdown.isFaceTracking is not True or self.dropdown.isQrCodeTracking is not True:
            self.capture.send_rc_control(0, 0, 0, 0)

    def rebound(self):
        while self.capture.get_height() > 50:
            self.capture.send_rc_control(0, 0, -50, 0)
        while self.capture.get_height() < 120:
            self.capture.send_rc_control(0, 0, 50, 0)
        while self.capture.get_height() > 80:
            self.capture.send_rc_control(0, 0, -50, 0)

    def round(self):
        self.capture.rotate_clockwise(360)

    def doCircle(self, direction):
        h = threading.Thread(name='circle', target=circle(51, direction, "cw", 0, 50, self.capture))
        h.start()

    def detectQrCode(self, img):
        det = decode(img)

        for barcode in det:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            if barcodeData is not None:
                h = threading.Thread(name='qrcode', target=self.capture.send_command_with_return(barcodeData))
                h.start()
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    def flip(self, direction):
        if self.flip_thread is not None:
            self.flip_thread.stop = False
            self.flip_thread = None
        self.flip_thread = threading.Thread(name='flip', target=self.threadFlip(direction))
        self.flip_thread.start()

    def threadFlip(self, direction):
        if direction == "l":
            self.capture.flip_left()
        elif direction == "r":
            self.capture.flip_right()
        elif direction == "f":
            self.capture.flip_forward()
        elif direction == "b":
            self.capture.flip_backwad()
        else:
            pass

    def findFace(self, img):
        cv2.circle(img, (int(self.width / 2), int(self.height / 2)), 10, (0, 255, 0))
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)

        myFaceListC = []
        myFaceListArea = []

        for (x, y, w, h) in faces:
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

    def trackFace(self, me, info, w, pid, pError):
        area = info[1]
        x, y = info[0]
        fb = 0

        error = x - w // 2
        speed = (pid[0] * error) + (pid[1] * (error - pError))
        speed = int(np.clip(speed, -100, 100))
        if self.FbRange[0] < area < self.FbRange[1]:
            fb = 0
        if area > self.FbRange[1]:
            fb = -20
        elif area < self.FbRange[0] and area != 0:
            fb = 20
        if x == 0:
            speed = 0
            error = 0

        me.send_rc_control(0, fb, 0, speed)
        return error

    def findQrCode(self, img):
        cv2.circle(img, (int(self.width / 2), int(self.height / 2)), 10, (0, 255, 0))
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

    # Move Forward
    def on_move_forward(self):
        if self.forward is not None:
            self.forward.stop = False
            self.forward = None
        self.forward = threading.Thread(name='move_forward', target=self.move_forward)
        self.forward.start()

    def move_forward(self):
        t = threading.currentThread()
        while getattr(t, "stop", True):
            self.capture.send_rc_control(0, 50, 0, 0)

    def off_move_forward(self):
        if self.forward is not None:
            self.forward.stop = False
            self.forward = None

    # Move Backward
    def on_move_backward(self):
        if self.backward is not None:
            self.backward.stop = False
            self.backward = None
        self.backward = threading.Thread(name='move_backward', target=self.move_backward)
        self.backward.start()

    def move_backward(self):
        t = threading.currentThread()
        while getattr(t, "stop", True):
            self.capture.send_rc_control(0, -50, 0, 0)

    def off_move_backward(self):
        if self.backward is not None:
            self.backward.stop = False
            self.backward = None

    # Move Right
    def on_move_right(self):
        if self.Right is not None:
            self.Right.stop = False
            self.Right = None
        self.Right = threading.Thread(name='move_right', target=self.move_right)
        self.Right.start()

    def move_right(self):
        t = threading.currentThread()
        while getattr(t, "stop", True):
            self.capture.send_rc_control(50, 0, 0, 0)

    def off_move_right(self):
        if self.Right is not None:
            self.Right.stop = False
            self.Right = None

    # Move left
    def on_move_left(self):
        if self.left is not None:
            self.left.stop = False
            self.left = None
        self.left = threading.Thread(name='move_left', target=self.move_left)
        self.left.start()

    def move_left(self):
        t = threading.currentThread()
        while getattr(t, "stop", True):
            self.capture.send_rc_control(-50, 0, 0, 0)

    def off_move_left(self):
        if self.left is not None:
            self.left.stop = False
            self.left = None

    # Move Up
    def on_move_up(self):
        if self.up is not None:
            self.up.stop = False
            self.up = None
        self.up = threading.Thread(name='move_up', target=self.move_up)
        self.up.start()

    def move_up(self):
        t = threading.currentThread()
        while getattr(t, "stop", True):
            self.capture.send_rc_control(0, 0, 50, 0)

    def off_move_up(self):
        if self.up is not None:
            self.up.stop = False
            self.up = None

    # Move Down
    def on_move_down(self):
        if self.down is not None:
            self.down.stop = False
            self.down = None
        self.down = threading.Thread(name='move_down', target=self.move_down)
        self.down.start()

    def move_down(self):
        t = threading.currentThread()
        while getattr(t, "stop", True):
            self.capture.send_rc_control(0, 0, -50, 0)

    def off_move_down(self):
        if self.down is not None:
            self.down.stop = False
            self.down = None

    # Rotate Right
    def on_move_rotateR(self):
        if self.rotateR is not None:
            self.rotateR.stop = False
            self.rotateR = None
        self.rotateR = threading.Thread(name='move_rotateR', target=self.move_rotateR)
        self.rotateR.start()

    def move_rotateR(self):
        t = threading.currentThread()
        while getattr(t, "stop", True):
            self.capture.send_rc_control(0, 0, 0, 50)

    def off_move_rotateR(self):
        if self.rotateR is not None:
            self.rotateR.stop = False
            self.rotateR = None

    # Rotate Left
    def on_move_rotateL(self):
        if self.rotateL is not None:
            self.rotateL.stop = False
            self.rotateL = None
        self.rotateL = threading.Thread(name='move_rotateL', target=self.move_rotateL)
        self.rotateL.start()

    def move_rotateL(self):
        t = threading.currentThread()
        while getattr(t, "stop", True):
            self.capture.send_rc_control(0, 0, 0, -50)

    def off_move_rotateL(self):
        if self.rotateL is not None:
            self.rotateL.stop = False
            self.rotateL = None

    def takeoff(self):
        h = threading.Thread(name='takeoff', target=self.takeoffThread)
        h.start()

    def takeoffThread(self):
        self.capture.takeoff()

    def land(self):
        h = threading.Thread(name='land', target=self.landThread)
        h.start()

    def landThread(self):
        self.capture.land()


class TelloApp(App):

    def __init__(self, tel, **kwargs):
        super(TelloApp, self).__init__(**kwargs)
        self.me = tel

    def build(self):
        self.me.connect()
        self.me.streamon()
        my_camera = KivyCamera(capture=self.me, fps=30)
        return my_camera

    def on_stop(self):
        self.me.streamoff()


if __name__ == '__main__':
    tell = tello.Tello()
    TelloApp(tell).run()
