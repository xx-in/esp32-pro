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

def ktv_random_color(duration=3):
    """模式 1：每个灯珠随机变色，快速跳动"""
    start_time = time.time()
    while time.time() - start_time < duration:
        for i in range(NUM_LEDS):
            # 从炫彩列表里随机选一个颜色给当前灯珠
            np[i] = urandom.choice(KTV_COLORS)
        np.write()
        time.sleep(0.15)  # 切换速度，越小越快

def ktv_chase(duration=3):
    """模式 2：经典的 KTV 动感跑马灯"""
    start_time = time.time()
    while time.time() - start_time < duration:
        color = urandom.choice(KTV_COLORS)  # 选一个主色
        for i in range(NUM_LEDS):
            clear_all()
            np[i] = color  # 单个灯珠亮起
            np.write()
            time.sleep(0.06)  # 跑马灯滚动速度

def ktv_strobe(duration=2):
    """模式 3：疯狂爆闪效果"""
    start_time = time.time()
    while time.time() - start_time < duration:
        color = urandom.choice(KTV_COLORS)
        # 全亮
        for i in range(NUM_LEDS):
            np[i] = color
        np.write()
        time.sleep(0.04)  # 亮起时间极短
        
        # 全灭
        clear_all()
        time.sleep(0.04)  # 熄灭时间极短

# 主循环：不断交替各种 KTV 效果
while True:
    print("KTV change...")
    # 执行随机色彩跳动 3 秒
    ktv_random_color(duration=3)
    
    # 执行动感跑马灯 3 秒
    ktv_chase(duration=3)
    
    # 执行激情爆闪 2 秒
    ktv_strobe(duration=2)
  
clear_all()