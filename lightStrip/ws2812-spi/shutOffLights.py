import spidev
import ws2812

spi = spidev.SpiDev()
spi.open(1,1)


leds = 50

info_to_write = []

for i in range(0, leds):
    info_to_write.append([0, 0, 0])

ws2812.write2812(spi, info_to_write)


