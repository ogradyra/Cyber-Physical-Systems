from microbit import *
import radio

radio.on()
radio.config(length=251)
radio.config(channel=23)
Msg = " "
count = 0
count_interval = 200
total = 0
battery:float = 0
total_battery:float = 0
avg_battery:float = 0
true_battery:float = 0

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

    command = radio.receive()

    #print(type(battery))

    if command:
        battery = float(command)

        display_battery_level(battery)

        total_battery = total_battery + battery

        print("Battery level:", (battery / 1023) * 3.3, "V")


        """if count % count_interval == 0:
            avg_battery = total_battery / count_interval
            true_battery = (avg_battery / 1023) * 3.3
            print("Battery level:", true_battery, "V")
            total_battery = 0

            if avg_battery < 300:
                print("LOW BATTERY RUNNING EMERGENCY PROTOCOLS")
                #emergency_safety_function() #run function when battery is low
                #break"""


    count += 1
