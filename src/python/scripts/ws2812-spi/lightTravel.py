import spidev
import ws2812
import time
import random
spi = spidev.SpiDev()
spi.open(1,1)


leds = 50

colors = [[255, 0, 0], [0,0,0], [0, 0, 255], [0,0,0], [255, 255, 0], [0,0,0],[0,0,0],[0,0,0]]

#write 4 WS2812's, with the following colors: red, green, blue, yellow
#ws2812.write2812(spi, [[10,0,0], [0,10,0], [0,0,10], [10, 10, 0]])

info_to_write = []

counter= -1
for i in range(0, leds):
    counter += 1
    info_to_write.insert(0, colors[counter % len(colors)])

ws2812.write2812(spi, info_to_write)

counter = 0
while True:

    #info_to_write.append([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])

    info_to_write.insert(0, colors[counter % len(colors)])

    if len(info_to_write) > leds:
        info_to_write.pop(leds)

    ws2812.write2812(spi, info_to_write)
    time.sleep(.5)
    counter += 1


