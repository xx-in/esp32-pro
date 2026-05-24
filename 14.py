from machine import Pin
import neopixel
import time
import urandom  # 用于产生随机数

# ws接口是用于控制rgb灯珠的，通常是单线接口，数据通过这个接口传输。ws2812b是常见的rgb灯珠型号，支持24位颜色控制（8位红色、8位绿色、8位蓝色）。每个灯珠可以独立设置颜色，通过串联多个灯珠，可以实现丰富的灯光效果。

# 定义引脚和灯珠数量
PIN_NUM = 15       
NUM_LEDS = 5       # 设定为 5 个灯珠

# 初始化 NeoPixel 对象
np = neopixel.NeoPixel(Pin(PIN_NUM, Pin.OUT), NUM_LEDS)

# KTV 常用高饱和度炫彩颜色列表
KTV_COLORS = [
    (255, 0, 0),     # 纯红
    (0, 255, 0),     # 纯绿
    (0, 0, 255),    # 纯蓝
    (255, 0, 255),   # 品红/紫
    (0, 255, 255),   # 青色
    (255, 255, 0),   # 黄色
    (255, 128, 0)    # 橙色
]

def clear_all():
    """全灭"""
    for i in range(NUM_LEDS):
        np[i] = (0, 0, 0)
    np.write()

clear_all()