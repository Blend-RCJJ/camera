import sensor
import image
import KPU as kpu
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
uart = UART(UART.UART1, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)

ws = ws2812(8,1)

#LED
#for LED in range(5):
r,g,b = 255,255,255
ws.set_led(0, (r,g,b))
ws.display()
time.sleep(0.1)

    #r,g,b = 0,0,0
    #ws.set_led(0, (r,g,b))
    #ws.display()
    #time.sleep(0.1)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
f = open('labels.txt', 'r')
labels = f.readlines()
f.close()
print(labels)

try:
    task = kpu.load("/sd/model.kmodel")
except:
    a=1

while(True):
    img = sensor.snapshot()

    # モデル入力用の画像サイズに変換
    img2 = img.resize(224, 224)
    # K210のRGB565 データを推論処理用のメモリブロック RGB888 にコピー
    img2.pix_to_ai()
    # モデルの実行
    fmap = kpu.forward(task, img2)

    plist = fmap[:]
#    print("plist:" + str(plist) )
    pmax = max(plist)
#    print("pmax:" + str(pmax) )
#   Avoiding Exception for index of undef result.
    if pmax >=0.8 and pmax <=1:
        max_index = plist.index(pmax)
        mozi = labels[max_index].strip()
        print(labels[max_index].strip())
        if mozi == "H":
            uart.write("H\n")
            time.sleep(5)
            uart.write("\n")
            time.sleep(5)

        if mozi == "S":
            uart.write("S\n")
            time.sleep(5)
            uart.write("\n")
            time.sleep(5)

        if mozi == "U":
            uart.write("U\n")
            time.sleep(5)
            uart.write("\n")
            time.sleep(5)

    else:
        print("N")


a = kpu.deinit(task)
