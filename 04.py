# 蜂鸣器
from machine import Pin
import time

# 对于具有负载的任何设备，都不能通过esp32的引脚直接供电，因为引脚的电流输出能力有限，通常在几十毫安左右，而蜂鸣器等设备可能需要更高的电流来正常工作。
# 此时需要驱动控制和电源分离的方式来控制蜂鸣器的状态。可以使用一个晶体管或一个继电器来实现这个功能。

# 对于蜂鸣器来说，通常需要将引脚设置为输出模式，并且在需要发声时将引脚设置为高电平，在不需要发声时将引脚设置为低电平。


beep = Pin(25, Pin.OUT, Pin.PULL_DOWN)

i = False

# 三秒钟后自动关闭

start_time = time.ticks_ms()

while True:
    # 检查是否已经过了三秒钟
    if time.ticks_diff(time.ticks_ms(), start_time) > 3000:
        beep.off()
        break

    i = not i
    if i:
        beep.on()
    else:
        beep.off()

    time.sleep_us(250)
    # 这个代码会让引脚25每隔250微秒切换一次状态，从而产生一个蜂鸣器的效果。
    # 250微秒的频率大约是4kHz，这个频率对于蜂鸣器来说是一个比较常见的发声频率，可以产生一个清晰的声音。
