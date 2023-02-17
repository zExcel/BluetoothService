import spidev
import ws2812
import time
import random
spi = spidev.SpiDev()
spi.open(1,1)


leds = 50

#write 4 WS2812's, with the following colors: red, green, blue, yellow
#ws2812.write2812(spi, [[10,0,0], [0,10,0], [0,0,10], [10, 10, 0]])


while True:

    info_to_write = []

    for i in range(0, leds):
        info_to_write.append([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])

    ws2812.write2812(spi, info_to_write)
    time.sleep(.01)


