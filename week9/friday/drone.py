# Add your Python code here. E.g.
from microbit import *
import radio
from math import *
import micropython
import time

uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=pin1, rx=pin8)
#uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=None, rx=None)

radio.on()
radio.config(length=251)
radio.config(channel=47)
radio.config(queue=1)
micropython.kbd_intr(-1)

x = 0
y = 0
z = 0
a = 0
t_flag = 0
incoming = 0

# function for splitting up incoming strings and assigning values for p,a,r,t,y
def receiver():
    global x, y, z, a, t_flag

    split_string = incoming.split(",")
    
    #print(incoming)
    
    # roll 
    x = int(split_string[0])
    # pitch
    y = int(split_string[1])
    # height
    z = int(split_string[2])
    # arm 
    a = int(split_string[3])
    
    t_flag = int(split_string[4])
    
    #print("x: ", x, " y: ", y, " z: ", z, " a: ", a)
    
    # LED to show when drone is armed
    if a > 0:
        display.set_pixel(0, 0, 9)
    else:
        display.set_pixel(0, 0, 0)
   

def getError(height):
    height_wanted = 40
    #print("height_wanted ", height_wanted, "Height ", height)
    error = height_wanted - height
    return error
   
def driver(pitch, roll, throttle):
    
    # scaling
    p_int = int( 3.5 * pitch + 512)
    r_int = int( 3.5 * roll  + 521)
    t_int = int((512 * throttle)/50)
    y_int = 512
    f_mode = 45*5
   
    arm = 900*a
    
    print("P: ", p_int, " A: ", arm, " R: ", r_int, " T: ", t_int, " Y: ", y_int)

    buf = bytearray(16)
    buf[0] = 0
    buf[1] = 0x01
    buf[2] = (0 << 2) | ((r_int >> 8) & 3)
    buf[3] = r_int & 255
    buf[4] = (1 << 2) | ((p_int >> 8) & 3)
    buf[5] = p_int & 255
    buf[6] = (2 << 2) | ((t_int >> 8) & 3)
    buf[7] = t_int & 255
    buf[8] = (3 << 2) | ((y_int >> 8) & 3)
    buf[9] = y_int & 255
    buf[10] = (4 << 2) | ((arm >> 8) & 3)
    buf[11] = arm & 255
    buf[12] = (5 << 2) | ((f_mode >> 8) & 3)
    buf[13] = f_mode & 255
    buf[14] = (6 << 2) | ((0 >> 8) & 3)
    buf[15] = 0 & 255
   
    uart.write(buf)
    print(buf)
   
while True:
   
    incoming = radio.receive()
   
    if incoming:
        receiver()
        if t_flag == 1:
            t_error = getError(z)
        else:
            t_error = 0
        #print("Error: ", t_error, "Flag: ", t_flag)
        driver(x,y,t_error)
        sleep(50)
    else:
        print("No Incoming Data")
