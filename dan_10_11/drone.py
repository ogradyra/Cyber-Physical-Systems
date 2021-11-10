# Add your Python code here. E.g.
from microbit import *
import radio
from math import *
import micropython
import time

#uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=pin1, rx=pin8)
uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=None, rx=None)

radio.on()
radio.config(length=251)
radio.config(channel=48)
radio.config(queue=1)
micropython.kbd_intr(-1)

x = 0
y = 0
z = 0
a = 0

incoming = 0

# function for splitting up incoming strings and assigning values for p,a,r,t,y
def receiver():
    global x, y, z, a

    split_string = incoming.split(",")
   
    print(incoming)

    x = int(split_string[0])
    y = int(split_string[1])
    z = int(split_string[2])
    a = int(split_string[3])
   
    print("x: ", x, " y: ", y, " z: ", z, " a: ", a)
   
    if a > 0:
        display.set_pixel(0, 0, 9)
    else:
        display.set_pixel(0, 0, 0)
   
# PID for X-direction control
xE = 0
xI = 0
def xPID(xKp, xKi, xKd):
    global xE, xI
    error = 0 - x
    
    xP = error
    xI += error
    xD = error - xE
    
    xE = error
    
    roll = xKp*xP + xKi*xI + xKd*xD
    
    return roll
    
# PID for Y-direction control
yE = 0
yI = 0
def yPID(yKp, yKi, yKd):
    global yE, yI
    error = 0 - y
    
    yP = error
    yI += error
    yD = error - yE
    
    yE = error
    
    pitch = yKp*yP + yKi*yI + yKd*yD
    
    return pitch  
    
# PID for Z-direction control
zE = 0
zI = 0
def zPID(zKp, zKi, zKd):
    global zE, zI
    error = 40 - z
    
    zP = error
    zI += error
    zD = error - zE
    
    zE = error
    
    throttle = zKp*zP + zKi*zI + zKd*zD
    
    return throttle  
 
   
def driver(pitch, roll, throttle):

    p_int = int( 3.5 * pitch + 512)
    r_int = int( 3.5 * roll  + 521)
    t_int = int((512 * throttle)/50)
    y_int = 512
   
    arm = 900*a
   
    #print("P: ", p_int, " A: ", arm, " R: ", r_int, " T: ", t_int, " Y: ", y_int)

    buf = bytearray(16)
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
        roll = 0 #xPID(1, 0, 0)
        pitch = 0  #yPID(1, 0, 0)
        throttle = zPID(1, 0, 0)
        driver(pitch, roll, throttle)
        sleep(50)
    else:
        print("No Incoming Data")
