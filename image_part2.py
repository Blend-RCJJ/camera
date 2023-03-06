import sensor
import image
#import lcd
import json
import time
import utime
from machine import UART
from Maix import GPIO
from fpioa_manager import *
from modules import ws2812

#uart setup
fm.register(34,fm.fpioa.UART1_TX)
fm.register(35,fm.fpioa.UART1_RX)
uart_out = UART(UART.UART1, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)

ws = ws2812(8,1)

#LED
for LED in range(5):
    r,g,b = 100,100,100
    ws.set_led(0, (r,g,b))
    ws.display()
    time.sleep(0.1)

    r,g,b = 0,0,0
    ws.set_led(0, (r,g,b))
    ws.display()
    time.sleep(0.1)

#camera setup
#lcd.init(freq=15000000)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
sensor.set_vflip(180)

#color serup
green_threshold  =  (13, 49, -41, -10, 3, 41)
red_threshold  =  (0, 41, 48, 60, 39, 53)
yellow_threshold  =  (47, 71, -24, -7, 33, 59)

black_threshold = (0, 2, -3, 2, -1, 2)

while True:
    img=sensor.snapshot()

    blobs1 = img.find_blobs([green_threshold])
    blobs2 = img.find_blobs([red_threshold])
    blobs3 = img.find_blobs([yellow_threshold])

    blobs4 = img.find_blobs([black_threshold])

    #color find
    if blobs1:
        for b in reversed(blobs1):
            if (b[2]*b[3] > 15000):
                uart_out.write('G\n')

        continue

    if blobs2:
        for b in reversed(blobs2):
            if (b[2]*b[3] > 15000):
                uart_out.write('R\n')

        continue

    if blobs3:
        for b in reversed(blobs3):
            if (b[2]*b[3] > 15000):
                uart_out.write('B\n')

        continue

    #letter setup
    if blobs4:
        for i in reversed(blobs4):
            if (i[2]*i[3] < 1000):

                uart_out.write('T\n')
                print('STOP')
                time.sleep(1)

                lines = img.find_lines(threshold = 1500, max_theta_difference = 10)
                A = len(lines)

                circles = img.find_circles(threshold = 1500, max_theta_difference = 10)
                B = len(circles)

                print(A)
                print(B)

                if(A >= 3 and A < 5 and B >= 3 and B <= 12):
                    uart_out.write('U\n')
                    print("U")

                    continue

                if(A > 3 and B >= 0):
                    uart_out.write('H\n')
                    print("H")

                    continue

                if(A <= 2 and B >= 13):
                    uart_out.write('S\n')
                    print('S')

                    continue

