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

# function for splitting up incoming strings and assigning values for p,a,r,t,y
def receive_data():
    global pitch, roll, throttle, arm, yaw

    split_string = incoming.split("_")

    for i in range(len(split_string)):
        if split_string[i] == "P":
            pitch = split_string[i + 1]

        elif split_string[i] == "A":
            arm = split_string[i + 1]

        elif split_string[i] == "R":
            roll = split_string[i + 1]

        elif split_string[i] == "T":
            throttle = split_string[i + 1]

        elif split_string[i] == "Y":
            yaw = split_string[i + 1]
        
        # print(split_string[i])

def read_into():

    p_int = int(pitch)
    r_int = int(roll)
    t_int = int(throttle)
    y_int = 512
    
    if arm == "1":
        a_int = 900
    else:
        a_int = 0

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
    buf[10] = (4 << 2) | ((a_int >> 8) & 3)
    buf[11] = a_int & 255
    buf[12] = (5 << 2) | ((225 >> 8) & 3)
    buf[13] = 225 & 255
    buf[14] = (6 << 2) | ((0 >> 8) & 3)
    buf[15] = 0 & 255
    
    uart.write(buf)
    #print(buf)
    
while True:
    
    incoming = radio.receive()
    
    if incoming:
        receive_data()
        read_into()
        sleep(50)
    else:
        print("No Incoming Data")
    