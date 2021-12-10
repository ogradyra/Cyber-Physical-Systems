# Add your Python code here. E.g.
from microbit import *
import radio
from math import *
import micropython
import utime

uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=pin1, rx=pin2)
#uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=None, rx=None)

radio.on()
radio.config(length=251)
radio.config(channel=47)
radio.config(queue=1)
micropython.kbd_intr(-1)

targetx  = 0
targety  = 0
height   = 0
a        = 0
t_flag   = 0
Pitchtel = 0
Rolltel  = 0
incoming = 0

buf = bytearray(16)

def battery_read():
    battery = pin0.read_analog()
    
    charge = ((battery-300)/(1023-300))
    if charge >= 0.6 and charge < 0.8:
        display.set_pixel(4, 0, 0)
        display.set_pixel(4, 1, 9)
        display.set_pixel(4, 2, 9)
        display.set_pixel(4, 3, 9)
        display.set_pixel(4, 4, 9)

    elif charge >= 0.4 and charge < 0.6:
        display.set_pixel(4, 0, 0)
        display.set_pixel(4, 1, 0)
        display.set_pixel(4, 2, 9)
        display.set_pixel(4, 3, 9)
        display.set_pixel(4, 4, 9)

    elif charge >= 0.2 and charge < 0.4:
        display.set_pixel(4, 0, 0)
        display.set_pixel(4, 1, 0)
        display.set_pixel(4, 2, 0)
        display.set_pixel(4, 3, 9)
        display.set_pixel(4, 4, 9)

    elif charge < 0.2:
        display.show(Image.SKULL)

    else:
        display.set_pixel(4, 0, 9)
        display.set_pixel(4, 1, 9)
        display.set_pixel(4, 2, 9)
        display.set_pixel(4, 3, 9)
        display.set_pixel(4, 4, 9)

# function for splitting up incoming strings and assigning values for p,a,r,t,y
def receiver():
    global targetx, targety, throttle, a

    split_string = incoming.split(",")
    
    targetx = int(split_string[0])
    targety = int(split_string[1])
    height  = int(split_string[2])
    a       = int(split_string[3])
    t_flag  = int(split_string[4])
    
    if a > 0:
        display.set_pixel(0, 0, 9)
    else:
        display.set_pixel(0, 0, 0)
 
def accelerometer_feedback():
    global Pitchtel, Rolltel

    if uart.any():
        data = uart.read()
        datalist = list(data)
        if isinstance(datalist, list) and len(datalist) >= 9:
            Pitchtel = int(datalist[3]) - int(datalist[4])
            Rolltel  = int(datalist[5]) - int(datalist[6])

# PID for X-direction control
xE = 0
xI = 0
def xPID(x, xKp, xKi, xKd, offset):
    global xE, xI
    
    error = targetx + offset - x
  
    xD = error - xE #Difference between the errors (new - old error)
    
    #Low-Pass Filter
    if abs(xD) > 10:
        temp = error
        error = xE
        xE = temp
        xD = 0
    
    xP = error
    xI += error
    
    xE = error
    
    roll = xKp*xP + xKi*xI + xKd*xD
    
    if roll > 85:
        roll = 85
    if roll < -85:
        roll = -85
    
    return roll
    
# PID for Y-direction control
yE = 0
yI = 0
def yPID(y, yKp, yKi, yKd, offset):
    global yE, yI
    
    error = targety + offset - y
    
    yD = error - yE #Difference between the errors (new - old error)
    
    #Low-Pass Filter
    if abs(yD) > 10:
        temp = error
        error = yE
        yE = temp
        yD = 0
    
    yP = error
    yI += error
    
    yE = error

    pitch = yKp*yP + yKi*yI + yKd*yD
    
    if pitch > 85:
        pitch = 85
    if pitch < -85:
        pitch = -85
    
    return pitch  

# PID for Z-direction control
zE = 0
zI = 0
def zPID(z, zKp, zKi, zKd):
    global zE, zI
    
    error = 45 - z
    
    zP = error
    zI += error
    zD = error - zE
    
    zE = error
    
    throttle = zKp*zP + zKi*zI + zKd*zD
    
    if throttle > 95:
        throttle = 95
    if throttle < 0:
        throttle = 0
    
    return throttle

# Function for writing values to the control board
def driver(pitch, roll, throttle):

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

# Infinite Loop
while True:
    incoming = radio.receive()

    if incoming:
        receiver()
        accelerometer_feedback()
        
        if t_flag == 1:
            roll     = xPID(Rolltel, 1, 0.01, 0.5, -2.2)
            pitch    = yPID(Pitchtel, 1, 0.01, 0.5, 2.6)
            throttle = zPID(height, 2, 0, 0)
        else:
            roll     = 0
            pitch    = 0
            throttle = 0
            zE = 0
            zI = 0
            xE = 0
            xI = 0
            yE = 0
            yI = 0
        
        driver(pitch, roll, throttle)
        battery_read()
        sleep(50) 