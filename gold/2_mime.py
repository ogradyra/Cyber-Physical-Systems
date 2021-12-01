# Add your Python code here. E.g.
from microbit import *
import radio
from math import *
import micropython
import utime

uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=pin1, rx=pin2)
#uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=None, rx=None)
buf = bytearray(16)

radio.on()
radio.config(length=251)
radio.config(channel=49)
radio.config(queue=1)
micropython.kbd_intr(-1)

p = 0
r = 0
t = 0
a = 0

def receiver():
    global p, r, t, a
    split_string = incoming.split(",")
    
    if split_string[0] == '2':
        print(split_string)
        if split_string[1] == '0':
            p = int(split_string[2])
            r = float(split_string[3])
            t = int(split_string[4])
            a = int(split_string[5])
            #radio.send("0" + "," + "1" + "," + "1")

def send_telem():
    # [0 = Drone Adress, 1 = Message comes from Mime, Pitch, Roll]
    radio.send("0" + "," + "2" + "," + "1" + "," + "-1")
    #print("Sent")

def driver(roll, pitch, throttle, a):
    p_int = int( 3.5 * pitch + 512)
    r_int = int( 3.5 * roll  + 521)
    t_int = int((512 * throttle)/50)
    y_int = 512
   
    arm = 900*a
    #print("P: ", p_int, "A: ", arm, "R: ", r_int, "T: ", t_int);
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
        send_telem()
        driver(r, p, t, a)
        if a > 0:
            display.set_pixel(0, 0, 9)
        else:
            display.set_pixel(0, 0, 0)
        sleep(50) #Sleep of 100 means we read the first 5/10 commands from drone and then stop seeing them after the sleep
