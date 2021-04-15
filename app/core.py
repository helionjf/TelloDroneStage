from kivy.app import App
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.core.window import Window
from djitellopy import tello
import cv2
import threading

# Kivy Camera permet d'afficher la camera ainsi que de gerer les bouttons
class KivyCamera(Image):

    def __init__(self, capture, fps, **kwargs):
        self.capture = capture
        self.forward = None
        self.backward = None
        self.left = None
        self.Right = None
        self.up = None
        self.down = None
        self.rotateR = None
        self.rotateL = None
        super(KivyCamera, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down, on_key_up=self._on_keyboard_up)
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
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = image_texture
        self.ids.battery_label.text = "Battery: " + str(self.capture.get_battery()) + "%"
        self.ids.temperature_label.text = "Temperature: " + str(self.capture.get_temperature()) + "°C"
        self.ids.barometer_label.text = "Altitude: " + str(self.capture.get_height()) + "cm"
        self.ids.time_flight_label.text = "Flight Time: " + str(self.capture.get_flight_time()) + "s"
        self.capture.send_rc_control(0, 0, 0, 0)

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
