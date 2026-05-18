from machine import Pin, Timer
import time


# 初始化15引脚为输出模式，并拉低
dc_motor = Pin(15, Pin.OUT, Pin.PULL_DOWN)

# 定义一个定时器回调函数，每次定时器触发时调用这个函数
def timer_callback(timer):
    # 切换引脚的状态（如果当前是高电平，就切换为低电平；如果当前是低电平，就切换为高电平）
    dc_motor.value(not dc_motor.value())         

# 创建一个定时器对象
# 注意：在很多平台上（如 ESP32），Timer(-1) 可能会报错。
# 这里改用 ID 为 0 的硬件定时器，或者在某些平台（如 RP2 / Pico）可以直接使用 Timer() 不传参。
timer = Timer(0)

# 设置定时器周期为500毫秒（0.5秒），并指定回调函数
timer.init(period=500, mode=Timer.PERIODIC, callback=timer_callback)

# 主循环可以执行其他任务，或者让芯片休眠
while True:
    time.sleep(1)  # 模拟主循环在做别的事情，或者单纯休眠节能