from microbit import *
import radio
import utime

radio.on()
radio.config(power = 7)
radio.config(channel=6)

Pitch = 0
Yaw = 0
Roll = 0
Throttle = 0
Arm = 0

start = 0


while True:

    values = ""

#Arming the drone
    if button_a.is_pressed() and button_b.is_pressed():
        if utime.ticks_diff(utime.ticks_ms(), start) > 500:
            start = utime.ticks_ms()
            if Arm == 1:
                Arm = 0
                Throttle = 0
                display.set_pixel(2, 2, 0)
            else:
                Arm = 1
                display.set_pixel(2, 2, 9)

#Failsafe
    if accelerometer.was_gesture("shake"):
        Arm = 0
        display.set_pixel(2, 2, 0)

#Controlling the throttle
    if button_b.was_pressed():
        if Throttle < 100:
            Throttle = Throttle + 5
        else:
            Throttle = 100
    if button_a.was_pressed():
        if Throttle > 0:
            Throttle = Throttle - 5
        else:
            Throttle = 0

#Controlling pitch and roll
    axis_y = accelerometer.get_y()
    axis_x = accelerometer.get_x()

    if axis_x > 300:
        Roll = 30
    elif axis_x < -300:
        Roll = -30
    else:
        Roll = 0

    if axis_y < -300:
        Pitch = 30
    elif axis_y > 300:
        Pitch = -30
    else:
        Pitch = 0

    values = str(Pitch) + "|" + "0" + "|" + str(Roll) + "|" + str(Throttle) + "|" + str(Arm)

    radio.send(values)
    #print(values)
    sleep(50)
