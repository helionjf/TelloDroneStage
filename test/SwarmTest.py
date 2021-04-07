from djitellopy import TelloSwarm
import cv2

swarm = TelloSwarm.fromIps([
    "192.168.137.205",
    "192.168.137.138"
])

swarm.connect()
swarm.takeoff()
swarm.streamon()

while True:
    img = {}
    for tello in swarm:
        img = tello.get_frame_read().frame
        for i in img:
            img = cv2.resize(img, (360, 240))
            cv2.imshow("Test", img)
            cv2.waitKey(1)

swarm.move_up(100)

swarm.sequential(lambda i, tello: tello.move_forward(20))

swarm.parallel(lambda i, tello: tello.move_left(100))

swarm.land()
swarm.end()
