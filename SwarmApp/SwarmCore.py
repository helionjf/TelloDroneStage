import threading
import socket
from kivy import Config
from kivy.clock import Clock
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty
from time import sleep


class Event(Widget):
    isDrone1 = BooleanProperty(False)
    isDrone2 = BooleanProperty(False)
    isDrone3 = BooleanProperty(False)
    isDrone4 = BooleanProperty(False)
    isDrone5 = BooleanProperty(False)
    isDrone6 = BooleanProperty(False)
    isDrone7 = BooleanProperty(False)
    isDrone8 = BooleanProperty(False)
    BoolList = [isDrone1, isDrone2, isDrone3, isDrone4, isDrone5, isDrone6, isDrone7, isDrone8]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drone = None
        self.abord_flag = None
        self.left = None
        self.Right = None
        self.forward = None
        self.backward = None
        self.up = None
        self.down = None
        self.rotate_right = None
        self.rotate_left = None
        self.flip_forward = None
        self.flip_backward = None
        self.flip_right = None
        self.flip_left = None
        self.oui = False
        self.takeoff = False
        self.search = True
        self.ipList = []
        self.tmp = 0
        self.local_ip = ''
        self.local_port = 8889
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
        self.socket.bind((self.local_ip, self.local_port))
        self.response = None
        self.receive_thread = threading.Thread(target=self._receive_thread_first)
        self.receive_thread.daemon = True
        self.receive_thread.start()
        Clock.schedule_interval(self.update, 1.0 / 30)

    def _receive_thread_first(self):
        t = threading.currentThread()
        while getattr(t, "stop", True):
            try:
                self.response, ip = self.socket.recvfrom(1024)
                if self.response == b'ok' and self.search is True:
                    print("receive: " + str(self.response) + " " + str(ip))
                    self.ipList.append(ip)
                else:
                    print("receive: " + str(self.response) + " " + str(ip))
            except socket.error as exc:
                print("Caught exception socket.error : %s" % exc)

    def update(self, dt):
        if self.tmp == 0:
            h = threading.Thread(name="ipsearch", target=self.droneIpSearch)
            h.start()
            self.tmp = 1
        self.checkNbDrone()
        if self.oui is not True:
            self.sendCommandToAllDrone("rc 0, 0, 0, 0")

    def land(self):
        if self.takeoff is True:
            h = threading.Thread(name='land', target=self.landThread)
            h.start()
            self.takeoff = False

    def landThread(self):
        self.sendCommandToAllDrone("land")

    def takeOff(self):
        if self.takeoff is False:
            h = threading.Thread(name='takeoff', target=self.takeOffThread)
            h.start()
            self.takeoff = True

    def takeOffThread(self):
        self.sendCommandToAllDrone("takeoff")

    def moveLeftOneDrone(self, nb):
        if self.left is not None and self.takeoff is True:
            self.left.stop = False
            self.left = None
        self.left = threading.Thread(name='move_left', target=self.moveLeftOneDroneThread, args=(nb,))
        self.left.start()
        self.oui = True

    def moveLeftOneDroneThread(self, nb):
        t = threading.currentThread()
        while getattr(t, "stop", True):
            self.sendCommandToIp("rc -25 0 0 0", self.ipList[nb])

    def moveLeftOneDroneUp(self):
        if self.left is not None and self.takeoff is True:
            self.left.stop = False
            self.left = None
            self.oui = False

    def moveRightOneDrone(self, nb):
        if self.Right is not None and self.takeoff is True:
            self.Right.stop = False
            self.Right = None
        self.Right = threading.Thread(name='move_right', target=self.moveRightOneDroneThread, args=(nb,))
        self.Right.start()
        self.oui = True

    def moveRightOneDroneThread(self, nb):
        t = threading.currentThread()
        while getattr(t, "stop", True):
            self.sendCommandToIp("rc 25 0 0 0", self.ipList[nb])

    def moveRightOneDroneUp(self):
        if self.Right is not None and self.takeoff is True:
            self.Right.stop = False
            self.Right = None
            self.oui = False

    def moveForwardOneDrone(self, nb):
        if self.forward is not None and self.takeoff is True:
            self.forward.stop = False
            self.forward = None
        self.forward = threading.Thread(name='move_forward', target=self.moveForwardOneDroneThread, args=(nb,))
        self.forward.start()
        self.oui = True

    def moveForwardOneDroneThread(self, nb):
        t = threading.currentThread()
        while getattr(t, "stop", True):
            self.sendCommandToIp("rc 0 25 0 0", self.ipList[nb])

    def moveForwardOneDroneUp(self):
        if self.forward is not None and self.takeoff is True:
            self.forward.stop = False
            self.forward = None
            self.oui = False

    def moveBackwardOneDrone(self, nb):
        if self.backward is not None and self.takeoff is True:
            self.backward.stop = False
            self.backward = None
        self.backward = threading.Thread(name='move_backward', target=self.moveBackwardOneDroneThread, args=(nb,))
        self.backward.start()
        self.oui = True

    def moveBackwardOneDroneThread(self, nb):
        t = threading.currentThread()
        while getattr(t, "stop", True):
            self.sendCommandToIp("rc 0 -25 0 0", self.ipList[nb])

    def moveBackwardOneDroneUp(self):
        if self.backward is not None and self.takeoff is True:
            self.backward.stop = False
            self.backward = None
            self.oui = False

    def moveUpOneDrone(self, nb):
        if self.up is not None and self.takeoff is True:
            self.up.stop = False
            self.up = None
        self.up = threading.Thread(name='move_up', target=self.moveUpOneDroneThread, args=(nb,))
        self.up.start()
        self.oui = True

    def moveUpOneDroneThread(self, nb):
        t = threading.currentThread()
        while getattr(t, "stop", True):
            self.sendCommandToIp("rc 0 0 25 0", self.ipList[nb])

    def moveUpOneDroneUp(self):
        if self.up is not None and self.takeoff is True:
            self.up.stop = False
            self.up = None
            self.oui = False

    def moveDownOneDrone(self, nb):
        if self.down is not None and self.takeoff is True:
            self.down.stop = False
            self.down = None
        self.down = threading.Thread(name='move_down', target=self.moveDownOneDroneThread, args=(nb,))
        self.down.start()
        self.oui = True

    def moveDownOneDroneThread(self, nb):
        t = threading.currentThread()
        while getattr(t, "stop", True):
            self.sendCommandToIp("rc 0 0 -25 0", self.ipList[nb])

    def moveDownOneDroneUp(self):
        if self.down is not None and self.takeoff is True:
            self.down.stop = False
            self.down = None
            self.oui = False

    def moveRotateRightOneDrone(self, nb):
        if self.rotate_right is not None and self.takeoff is True:
            self.rotate_right.stop = False
            self.rotate_right = None
        self.rotate_right = threading.Thread(name='move_rotate_right', target=self.moveRotateRightOneDroneThread, args=(nb,))
        self.rotate_right.start()
        self.oui = True

    def moveRotateRightOneDroneThread(self, nb):
        t = threading.currentThread()
        while getattr(t, "stop", True):
            self.sendCommandToIp("rc 0 0 0 25", self.ipList[nb])

    def moveRotateRightOneDroneUp(self):
        if self.rotate_right is not None and self.takeoff is True:
            self.rotate_right.stop = False
            self.rotate_right = None
            self.oui = False

    def moveRotateLeftOneDrone(self, nb):
        if self.rotate_left is not None and self.takeoff is True:
            self.rotate_left.stop = False
            self.rotate_left = None
        self.rotate_left = threading.Thread(name='move_rotate_left', target=self.moveRotateLeftOneDroneThread, args=(nb,))
        self.rotate_left.start()
        self.oui = True

    def moveRotateLeftOneDroneThread(self, nb):
        t = threading.currentThread()
        while getattr(t, "stop", True):
            self.sendCommandToIp("rc 0 0 0 -25", self.ipList[nb])

    def moveRotateLeftOneDroneUp(self):
        if self.rotate_left is not None and self.takeoff is True:
            self.rotate_left.stop = False
            self.rotate_left = None
            self.oui = False

    def moveFlipForwardOneDrone(self, nb):
        if self.flip_forward is not None and self.takeoff is True:
            self.flip_forward.stop = False
            self.flip_forward = None
        self.flip_forward = threading.Thread(name='move_flip_forward', target=self.moveFlipForwardOneDroneThread, args=(nb,))
        self.flip_forward.start()
        self.oui = True

    def moveFlipForwardOneDroneThread(self, nb):
        self.sendCommandToIp("flip f", self.ipList[nb])

    def moveFlipForwardOneDroneUp(self):
        if self.flip_forward is not None and self.takeoff is True:
            self.flip_forward.stop = False
            self.flip_forward = None
            self.oui = False

    def moveFlipBackwardOneDrone(self, nb):
        if self.flip_backward is not None and self.takeoff is True:
            self.flip_backward.stop = False
            self.flip_backward = None
        self.flip_backward = threading.Thread(name='move_flip_backward', target=self.moveFlipBackwardOneDroneThread, args=(nb,))
        self.flip_backward.start()
        self.oui = True

    def moveFlipBackwardOneDroneThread(self, nb):
        self.sendCommandToIp("flip b", self.ipList[nb])

    def moveFlipBackwardOneDroneUp(self):
        if self.flip_backward is not None and self.takeoff is True:
            self.flip_backward.stop = False
            self.flip_backward = None
            self.oui = False

    def moveFlipRightOneDrone(self, nb):
        if self.flip_right is not None and self.takeoff is True:
            self.flip_right.stop = False
            self.flip_right = None
        self.flip_right = threading.Thread(name='move_flip_right', target=self.moveFlipRightOneDroneThread, args=(nb,))
        self.flip_right.start()
        self.oui = True

    def moveFlipRightOneDroneThread(self, nb):
        self.sendCommandToIp("flip r", self.ipList[nb])

    def moveFlipRightOneDroneUp(self):
        if self.flip_right is not None and self.takeoff is True:
            self.flip_right.stop = False
            self.flip_right = None
            self.oui = False

    def moveFlipLeftOneDrone(self, nb):
        if self.flip_left is not None and self.takeoff is True:
            self.flip_left.stop = False
            self.flip_left = None
        self.flip_left = threading.Thread(name='move_flip_left', target=self.moveFlipLeftOneDroneThread, args=(nb,))
        self.flip_left.start()
        self.oui = True

    def moveFlipLeftOneDroneThread(self, nb):
        self.sendCommandToIp("flip l", self.ipList[nb])

    def moveFlipLeftOneDroneUp(self):
        if self.flip_left is not None and self.takeoff is True:
            self.flip_left.stop = False
            self.flip_left = None
            self.oui = False

    def checkNbDrone(self):
        if len(self.ipList) > 0:
            self.isDrone1 = BooleanProperty(True)
        if len(self.ipList) > 1:
            self.isDrone2 = BooleanProperty(True)
        if len(self.ipList) > 2:
            self.isDrone3 = BooleanProperty(True)
        if len(self.ipList) > 3:
            self.isDrone4 = BooleanProperty(True)
        if len(self.ipList) > 4:
            self.isDrone5 = BooleanProperty(True)
        if len(self.ipList) > 5:
            self.isDrone6 = BooleanProperty(True)
        if len(self.ipList) > 6:
            self.isDrone7 = BooleanProperty(True)
        if len(self.ipList) > 7:
            self.isDrone8 = BooleanProperty(True)

    def sendCommandToIp(self, cmd, ip):
        print("Send Command: " + cmd + " to " + str(ip))
        self.socket.sendto(cmd.encode('utf-8'), ip)

    def sendCommandToAllDrone(self, cmd):
        print("Send Command: " + cmd + " to all Drone")
        if len(self.ipList) > 0:
            self.socket.sendto(cmd.encode('utf-8'), self.ipList[0])
        if len(self.ipList) > 1:
            self.socket.sendto(cmd.encode('utf-8'), self.ipList[1])
        if len(self.ipList) > 2:
            self.socket.sendto(cmd.encode('utf-8'), self.ipList[2])
        if len(self.ipList) > 3:
            self.socket.sendto(cmd.encode('utf-8'), self.ipList[3])
        if len(self.ipList) > 4:
            self.socket.sendto(cmd.encode('utf-8'), self.ipList[4])
        if len(self.ipList) > 5:
            self.socket.sendto(cmd.encode('utf-8'), self.ipList[5])
        if len(self.ipList) > 6:
            self.socket.sendto(cmd.encode('utf-8'), self.ipList[6])
        if len(self.ipList) > 7:
            self.socket.sendto(cmd.encode('utf-8'), self.ipList[7])

    def droneIpSearch(self):
        i = 0
        while i < 256:
            self.abord_flag = False
            timer = threading.Timer(.01, self.set_abord_flag)
            telloAdress = ("192.168.137." + str(i), 8889)
            self.socket.sendto(b'command', telloAdress)
            timer.start()
            while self.response is None:
                if self.abord_flag is True:
                    break
            timer.cancel()
            self.response = None
            i += 1
        print(self.ipList)
        self.search = False

    def set_abord_flag(self):
        self.abord_flag = True


class MySwarmApp(App):
    def build(self):
        my_event = Event()
        return my_event


if __name__ == "__main__":
    tmp = MySwarmApp()
    tmp.run()
