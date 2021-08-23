import threading
import socket
import time
import nums_from_string


class Choregraphie:
    def __init__(self):
        self.abord_flag = None
        self.local_ip = ''
        self.local_port = 8889
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.local_ip, self.local_port))
        self.ipList = []
        self.response = None
        self.search = True
        self.receive_thread = threading.Thread(target=self._receive_thread_first)
        self.receive_thread.daemon = True
        self.receive_thread.start()
        self.droneIpSearch()
        self.runDemo()

    def runDemo(self):
        self.checkStart()
        self.sendCommandToAllDrone("takeoff")
        time.sleep(7)
        self.sendCommandToIp("left 25", self.ipList[0])
        self.sendCommandToIp("right 25", self.ipList[1])
        time.sleep(5)
        self.sendCommandToIp("flip r", self.ipList[0])
        self.sendCommandToIp("flip l", self.ipList[1])
        time.sleep(5)
        self.sendCommandToIp("forward 50", self.ipList[0])
        self.sendCommandToIp("back 25", self.ipList[1])
        time.sleep(5)
        self.sendCommandToIp("down 25", self.ipList[0])
        self.sendCommandToIp("up 25", self.ipList[1])
        time.sleep(5)
        self.sendCommandToIp("right 25", self.ipList[0])
        self.sendCommandToIp("left 25", self.ipList[1])
        time.sleep(5)
        self.sendCommandToIp("flip b", self.ipList[0])
        self.sendCommandToIp("flip f", self.ipList[1])
        time.sleep(5)
        self.sendCommandToIp("cw 360", self.ipList[0])
        self.sendCommandToIp("ccw 360", self.ipList[1])
        time.sleep(10)
        self.sendCommandToIp("flip r", self.ipList[0])
        self.sendCommandToIp("flip l", self.ipList[1])
        time.sleep(5)
        self.sendCommandToIp("left 25", self.ipList[0])
        self.sendCommandToIp("right 25", self.ipList[1])
        time.sleep(5)
        self.sendCommandToIp("forward 25", self.ipList[0])
        self.sendCommandToIp("back 25", self.ipList[1])
        time.sleep(5)
        self.sendCommandToAllDrone("land")
        time.sleep(5)

    def checkStart(self):
        if len(self.ipList) != 2:
            print("Error you need 2 drones but you have only " + str(len(self.ipList)) + " drone connected")
            exit(84)
        self.sendCommandToIp("battery?", self.ipList[0])
        time.sleep(3)
        if nums_from_string.get_nums(str(self.response))[0] < 20:
            print("Error " + str(self.ipList[0]) + " does not have enough battery")
            exit(84)
        self.sendCommandToIp("battery?", self.ipList[1])
        time.sleep(3)
        if nums_from_string.get_nums(str(self.response))[0] < 20:
            print("Error " + str(self.ipList[1]) + " does not have enough battery")
            exit(84)
        self.sendCommandToIp("motoron", self.ipList[0])
        print("Put the drone without motor on on left")
        time.sleep(5)
        self.sendCommandToIp("motoron", self.ipList[1])
        time.sleep(5)

    def _receive_thread_first(self):
        t = threading.currentThread()
        while getattr(t, "stop", True):
            try:
                self.response, ip = self.socket.recvfrom(1024)
                if self.response == b'ok' and self.search is True:
                    print('\033[92m' + "receive: " + str(self.response) + " " + str(ip) + '\033[0m')
                    self.ipList.append(ip)
                elif self.response == b'ok':
                    print('\033[92m' + "receive: " + str(self.response) + " " + str(ip) + '\033[0m')
                else:
                    print('\033[91m' + "error receive: " + str(self.response) + " " + str(ip) + '\033[0m')
            except socket.error as exc:
                print('\033[91m' + "Caught exception socket.error : %s" % exc + '\033[0m')

    def sendCommandToIp(self, cmd, ip):
        print('\033[93m' + "Send Command: " + cmd + " to " + str(ip) + '\033[0m')
        self.socket.sendto(cmd.encode('utf-8'), ip)

    def sendCommandToAllDrone(self, cmd):
        print('\033[93m' + "Send Command: " + cmd + " to all Drone" + '\033[0m')
        if len(self.ipList) > 0:
            self.socket.sendto(cmd.encode('utf-8'), self.ipList[0])
        if len(self.ipList) > 1:
            self.socket.sendto(cmd.encode('utf-8'), self.ipList[1])

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


if __name__ == '__main__':
    Choregraphie()
