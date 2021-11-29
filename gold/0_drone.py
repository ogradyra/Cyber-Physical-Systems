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
radio.config(queue=5)
micropython.kbd_intr(-1)

x = 0
y = 0
z = 0
a = 0
t_flag = 0

Pitchtel = 0
Rolltel  = 0

incoming = 0
ACK = utime.ticks_ms()

buf = bytearray(16)

def battery_read():
    battery = pin0.read_analog()
    #print("Battery: ", battery)
    radio.send("1" + "," + "0" + "," + str(battery))
    
    charge = ((battery-300)/(1023-300))
    #print(charge)
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
    global x, y, z, a, t_flag

    split_string = incoming.split(",")
    
    if split_string[0] == '0':
        if split_string[1] == '1':
            print("ACK: ", split_string[2])
            ack(split_string[2])
        elif split_string[1] == '0':
            x = int(split_string[2])
            y = int(split_string[3])
            z = int(split_string[4])
            a = int(split_string[5])
            t_flag = int(split_string[6])
   
def ack(signal):
    global ACK
    if signal == '1':
        ACK = utime.ticks_ms()
        display.set_pixel(2, 2, 9)

def accelerometer_feedback():
    global Pitchtel, Rolltel
    
    #Rolltel = accelerometer.get_x()
    #Pitchtel = -accelerometer.get_y()
    
    if uart.any():
        data = uart.read()
        datalist = list(data)
        #display.show(Image.HEART)
        
        if isinstance(datalist, list) and len(datalist) >= 9:
            Pitchtel = int(datalist[3]) - int(datalist[4])
            Rolltel  = int(datalist[5]) - int(datalist[6])
        
    return Pitchtel, Rolltel

# sends roll and pitch values to the montior
def transmitter(p, r, t, a):
    message = "2" + "," + "0" + "," + str(p) + "," + str(r) + "," + str(t) + "," + str(a)
    radio.send(message)

# PID for X-direction control
xE = 0
xI = 0
def xPID(xKp, xKi, xKd):
    global xE, xI
    
    error = 0 - x
  
    xD = error - xE #Difference between the errors (new - old error)
    
    if abs(xD) > 5: #If error too big
        error = xE #Error doesn't change
        xD = 0 #Same so no difference to rate of change
    
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
def yPID(yKp, yKi, yKd):
    global yE, yI
    
    error = 0 - y
    
    yD = error - yE #Difference between the errors (new - old error)
    
    if abs(yD) > 5: #If error too big
        error = yE #Error doesn't change
        yD = 0 #Same so no difference to rate of change
    
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
def zPID(zKp, zKi, zKd):
    global zE, zI
    target_height = 45 #Have target range instead of target height
    #Have B pulses more than A pulses to counteract the lack of sensitivity for the downward pulses
    error = target_height - z

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
   
while True:
    incoming = radio.receive()

    if incoming:
        print("Incoming: ",incoming)
        receiver()
        x, y = accelerometer_feedback()
        
        if t_flag == 1:
            throttle = zPID(2, 0, 0)
            roll = xPID(0.5, 0.01, 1)
            pitch = yPID(0.5, 0, 1)
        else:
            throttle = 0
            roll = 0
            pitch = 0
            zE = 0
            zI = 0
            xE = 0
            xI = 0
            yE = 0
            yI = 0

        if a > 0:
            display.set_pixel(0, 0, 9)
        else:
            display.set_pixel(0, 0, 0)
            
        driver(pitch, roll, throttle)
        #transmitter(int(pitch), int(roll), throttle, a)
        #battery_read()
        sleep(10)
    #else:
        #print("No Incoming Data")
        
    if utime.ticks_diff(utime.ticks_ms(), ACK) >= 1000 or utime.ticks_diff(utime.ticks_ms(), ACK) < 0:
        #print("reset")
        display.set_pixel(2, 2, 0) # reset d, so this code can execute every 50 ms
        ACK = utime.ticks_ms()
