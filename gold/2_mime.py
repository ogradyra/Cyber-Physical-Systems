# Add your Python code here. E.g.
from microbit import *
import radio
from math import *
import micropython
import utime

#uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=pin1, rx=pin2)
uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=None, rx=None)
buf = bytearray(16)

radio.on()
radio.config(length=251)
radio.config(channel=47)
radio.config(queue=1)
micropython.kbd_intr(-1)

pitch = 0
roll = 0
throttle = 0
a = 0

def receiver():
    global pitch, roll, throttle, a
    split_string = incoming.split(",")
    
    print(split_string)
    if split_string[0] == '2':
        if split_string[1] == '0':
            pitch = int(split_string[2])
            roll = int(split_string[3])
            throttle = int(split_string[4])
            a = int(split_string[5])
            #radio.send("0" + "," + "1" + "," + "1")

def driver():

    p_int = int( 3.5 * pitch + 512)
    r_int = int( 3.5 * roll  + 521)
    t_int = int((512 * throttle)/50)
    y_int = 512
   
    arm = 900*a

    buf[0] = 0
    buf[1] = 0x01
    buf[2] = (0 << 2) | ((r_int >> 8) & 3)
    buf[3] = r_int & 255
    buf[4] = (1 << 2) | ((p_int >> 8) & 3)
    buf[5] = p_int & 255
    buf[6] = (2 << 2) | ((t_int >> 8) & 3)
    buf[7] = t_int & 255
    buf[8] = (3 << 2) | ((512 >> 8) & 3)
    buf[9] = 512 & 255
    buf[10] = (4 << 2) | ((arm >> 8) & 3)
    buf[11] = arm & 255
    buf[12] = (5 << 2) | ((225 >> 8) & 3)
    buf[13] = 225 & 255
    buf[14] = (6 << 2) | ((0 >> 8) & 3)
    buf[15] = 0 & 255
   
    uart.write(buf)

while True:
    incoming = radio.receive()
    
    if incoming:
        receiver()
        driver()
        if a > 0:
            display.set_pixel(0, 0, 9)
        else:
            display.set_pixel(0, 0, 0)
        sleep(50)
                
                
                
