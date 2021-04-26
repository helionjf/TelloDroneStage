from djitellopy import tello

me = tello.Tello()
me.connect()


while True:
    cmd = input('')
    me.send_command_without_return(cmd)
    if cmd == "end":
        me.land()
        me.end()
        break