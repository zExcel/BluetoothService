import spidev
import ws2812
import time
import random
import numpy as np
import cmapy
spi = spidev.SpiDev()
spi.open(1,1)

write=ws2812.write2812
leds = 50

#write 4 WS2812's, with the following colors: red, green, blue, yellow
#ws2812.write2812(spi, [[10,0,0], [0,10,0], [0,0,10], [10, 10, 0]])

lerp_steps = 6

def generate_random_color():
    return np.array([cmapy.color('hsv', random.randrange(0, 256), rgb_order=True)])

def find_lerp_array(current_color, desired_color):
    return (desired_color - current_color) / lerp_steps

def add_lerp_array(current_color, lerp_array):
    return (current_color + lerp_array).astype(int)

current_color = generate_random_color()
desired_color = generate_random_color()

lerp_array = find_lerp_array(current_color, desired_color)

values_to_write = np.array([current_color])

steps_remaining = lerp_steps
counter = 1
while True:
    current_color = add_lerp_array(current_color, lerp_array)
    if counter < leds:
        values_to_write = np.append(values_to_write, np.array([current_color]), axis=0)
    else:
        values_to_write[counter % leds] = current_color
    steps_remaining -= 1
    if (steps_remaining == 0):
        desired_color = generate_random_color()
        lerp_array = find_lerp_array(current_color, desired_color)
        steps_remaining = lerp_steps
    write(spi, values_to_write)
    counter += 1
    time.sleep(.2)



