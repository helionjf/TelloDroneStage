from djitellopy import TelloSwarm

swarm = TelloSwarm.fromIps([
    "192.168.137.225",
    "192.168.137.5"
])

swarm.connect()
# swarm.takeoff()
for tello in swarm:
    print(tello.get_battery())

swarm.move_up(100)

swarm.sequential(lambda i, tello: tello.move_forward(20))

swarm.parallel(lambda i, tello: tello.move_left(100))

swarm.land()
swarm.end()
