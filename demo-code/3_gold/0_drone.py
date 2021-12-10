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

a = 0
throttle = 0
targetx  = 0
targety  = 0

Pitchtel = 0
Rolltel  = 0

mime_pitch = 0
mime_roll  = 0

incoming = 0
ACK = utime.ticks_ms()

buf = bytearray(16)

xE1 = 0
xI1 = 0
yE1 = 0
yI1 = 0
xE2 = 0
xI2 = 0
yE2 = 0
yI2 = 0

def battery_read():
    battery = pin0.read_analog()
    radio.send("1" + "," + "0" + "," + str(battery))
    
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
    global targetx, targety, throttle, a, mime_pitch, mime_roll

    split_string = incoming.split(",")
    
    if split_string[0] == '0': #Drone is receiver of message
        if split_string[1] == '1': #Controller is sender of message
            targety = float(split_string[2])
            targetx = float(split_string[3])
            throttle= int(split_string[4])
            a       = int(split_string[5])
        elif split_string[1] == '2': #Mime is sender of message
            mime_roll = int(split_string[2])
            mime_pitch = int(split_string[3])
 
def accelerometer_feedback():
    global Pitchtel, Rolltel

    if uart.any():
        data = uart.read()
        datalist = list(data)
        if isinstance(datalist, list) and len(datalist) >= 9:
            Pitchtel = int(datalist[3]) - int(datalist[4])
            Rolltel  = int(datalist[5]) - int(datalist[6])

# Generic PID for XY-direction control
def PID(current, target, Kp, Ki, Kd, offset, E, I):

    error = target + offset - current
    
    #Difference between the errors (new - old error)
    D = error - E
    
    #Low-Pass Filter
    if abs(D) > 15:
        temp = error
        error = E
        E = temp
        D = 0
    
    P = error
    I += error
    
    E = error

    result = Kp*P + Ki*I + Kd*D
    
    if result > 85:
        result = 85
    if result < -85:
        result = -85
    
    return result, E, I  
   
def driver(pitch, roll, t):

    p_int = int( 3.5 * pitch + 512)
    r_int = int( 3.5 * roll  + 521)
    t_int = int((512 * t)/50)
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
        t = throttle
        accelerometer_feedback()
        
        #xPID(x, xKp, xKi, xKd, offset)
        roll, yE1, xI1  = PID(Rolltel, targetx, 1, 0.01, 0.5, -1.1, xE1, xI1)
        pitch, xE1, xI1 = PID(Pitchtel, targety, 1, 0.01, 0.5, 1.2, yE1, yE1)
        r, xE2, xI2 = PID(mime_roll, targetx, 1, 0.01, 0.5, 0.5, xE2, xI2)
        p, yE2, yI2 = PID(mime_pitch, targety, 1, 0.01, 0.5, 3, yE2, yE2)
    
        # [2 = Mime Address, 0 = Message comes from Drone, P, R, T, A]
        message = "2" + "," + "0" + "," + str(p) + "," + str(r) + "," + str(t) + "," + str(a)
        radio.send(message)
        
        driver(pitch, roll, t)
        
        if a > 0:
            display.set_pixel(0, 0, 9)
        else:
            display.set_pixel(0, 0, 0)
            xE1 = 0
            xI1 = 0
            yE1 = 0
            yI1 = 0
            xE2 = 0
            xI2 = 0
            yE2 = 0
            yI2 = 0
        
        battery_read()
        sleep(10) 
