from djitellopy import tello

me = tello.Tello()
me.connect()


while True:
    cmd = input('')
    print(me.send_command_with_return(cmd))
    if cmd == "end":
        me.land()
        me.end()
        break