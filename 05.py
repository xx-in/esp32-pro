from machine import Pin
import time
# 继电器分为三个口，NC（常闭），NO（常开）和COM（公共）。当继电器未通电时，NC和COM连接；当继电器通电时，NO和COM连接。
# NC的全称是Normally Closed，NO的全称是Normally Open，COM的全称是Common。

pin25 = Pin(25, Pin.OUT, Pin.PULL_DOWN)

# 将25引脚和rel连接，用于控制继电器
# 继电器NO

while True:
    pin25.on()
    print("继电器通电，NO和COM连接")
    time.sleep(1)
    pin25.off()
    print("继电器断电，NC和COM连接")
    time.sleep(1)
