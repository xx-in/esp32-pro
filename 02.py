# 这个代码是用来控制引脚15的输出状态的
# 实现了一个简单的闪烁效果，每隔1秒钟切换一次状态
from machine import Pin

# time模块提供了时间相关的函数，可以用来实现延时等功能
import time

p15 = Pin(15, Pin.OUT, Pin.PULL_DOWN)
while True:
    p15.on()
    time.sleep(1)
    p15.off()
    time.sleep(1)

# 这个代码会让引脚15每隔1秒钟切换一次状态，从而产生一个闪烁的效果。
