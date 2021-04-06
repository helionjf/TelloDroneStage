from time import sleep


# commande simple si le qrcode demo2 est reconnu

def demo2(me):
    me.set_speed(100)
    me.move_forward(50)
    sleep(2.2)
    me.rotate_clockwise(90)
    sleep(2.2)
    me.flip_forward()
    sleep(2.2)
    me.flip_back()
    sleep(2.2)
    me.rotate_counter_clockwise(90)
    sleep(2.2)
    me.move_back(50)
    sleep(2.2)
    return
