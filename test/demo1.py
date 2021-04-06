from time import sleep


# commande simple si le qrcode demo1 est reconnu

def demo1(me):
    me.set_speed(60)
    sleep(1)
    me.rotate_clockwise(360)
    sleep(7)
    me.rotate_counter_clockwise(360)
    sleep(7)
    me.move_up(50)
    sleep(2.2)
    me.move_down(100)
    sleep(3.5)
    me.move_up(50)
    sleep(2.2)
    me.flip_right()
    sleep(4)
    me.flip_left()
    sleep(4)
    return