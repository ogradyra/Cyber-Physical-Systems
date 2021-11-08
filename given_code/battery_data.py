#use with any code that receives radio messages
from microbit import *
import radio
#import utime
import micropython

#Initialising microbit
uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=pin1, rx=pin2)
#uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=None, rx=None)
radio.on()
radio.config(length=251)
radio.config(channel=23)
micropython.kbd_intr(-1)

Pitchtel = 0
Yawtel = 0
Rolltel = 0
datalet = 0
battery = 0
datalist =[]

def display_battery_level(b)->none:

    battery_percent = ((b-300)/(1023-300))

    if battery_percent >= 0.6 and battery_percent < 0.8:
        display.set_pixel(4,0,0)
        display.set_pixel(4,1,9)
        display.set_pixel(4,2,9)
        display.set_pixel(4,3,9)
        display.set_pixel(4,4,9)

    elif battery_percent >= 0.4 and battery_percent < 0.6:
        display.set_pixel(4,0,0)
        display.set_pixel(4,1,0)
        display.set_pixel(4,2,9)
        display.set_pixel(4,3,9)
        display.set_pixel(4,4,9)

    elif battery_percent >= 0.2 and battery_percent < 0.4:
        display.set_pixel(4,0,0)
        display.set_pixel(4,1,0)
        display.set_pixel(4,2,0)
        display.set_pixel(4,3,9)
        display.set_pixel(4,4,9)

    elif battery_percent < 0.2:
        display.show(Image.SKULL)

    else:
        display.set_pixel(4,0,9)
        display.set_pixel(4,1,9)
        display.set_pixel(4,2,9)
        display.set_pixel(4,3,9)
        display.set_pixel(4,4,9)

while True:
    battery = pin0.read_analog()
    display_battery_level(battery)
    radio.send(str(battery))  #battery is not used when connected via usb

    """#Reading from UART to get telemetry
    if uart.any():
        data = uart.read()
        datalist = list(data)

        if isinstance(datalist, list) and len(datalist) >= 9:
            Pitchtel = int(datalist[3]) - int(datalist[4])
            Rolltel = int(datalist[5]) - int(datalist[6])
            Yawtel = int(datalist[7]) + (int(datalist[8]) * 255)
            datalet = int(len(datalist))

    #putting together all telemetry and sending it back to the transmitter
    x = accelerometer.get_x()
    y = accelerometer.get_y()
    z = accelerometer.get_z()
    #telemetry = str(x) + ", " + str(y) + ", " + str(z) + ", " + str(Pitchtel) + ", " + str(Yawtel) + ", " + str(Rolltel) + ", " + str(running_time())+ ", " + str(datalet)
    telemetry = str(datalist)"""
    #radio.send(telemetry)
