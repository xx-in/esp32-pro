# 03.py
# 这个代码示例演示了如何使用machine模块控制多个引脚的状态
# 这个代码会让引脚15、2、0、4、16、17、5和18依次点亮，每个引脚点亮后等待0.05秒
# 然后再依次熄灭，每个引脚熄灭后也等待0.05秒。
from machine import Pin
import time

led_pin = [15, 2, 0, 4, 16, 17, 5, 18]
leds = []
# 初始化引脚，将它们设置为输出模式，并启用下拉电阻
for i in led_pin:
    p = Pin(i, Pin.OUT, Pin.PULL_DOWN, value=0)
    leds.append(p)

# 这个代码会让引脚15、2、0、4、16、17、5和18依次点亮，每个引脚点亮后等待0.05秒
# 然后再依次熄灭，每个引脚熄灭后也等待0.05秒。

while True:
    for i in range(8):
        leds[i].on()
        time.sleep(0.05)

    for i in range(8):
        leds[i].off()
        time.sleep(0.05)
