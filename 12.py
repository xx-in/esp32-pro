from machine import Pin, PWM
import time

# 1. 初始化引脚 15 为 PWM 输出 ，注意15号线要连接ws接口
pwm_pin = Pin(15, Pin.OUT)
led_pwm = PWM(pwm_pin)

# 2. 设置 PWM 的频率（Frequency）
# 频率设置为 1000Hz (1kHz) 足够高，肉眼完全看不出闪烁，适合调光
led_pwm.freq(1000)

# 定义呼吸灯的步进延迟（控制呼吸的速度，单位：秒）
DELAY = 0.005

while True:
    # 3. 逐渐变亮
    # MicroPython 的 PWM 占空比范围通常是 0 到 1023（10位分辨率）
    # 注意：某些特定固件（如 RP2040 的某些版本）可能是 0 到 65535，
    # 这里以最通用的 0-1023 为例。如果你的板子完全不亮，可尝试把最大值改为 65535。
    for duty_cycle in range(0, 1024, 8):
        led_pwm.duty(duty_cycle)  # 设置占空比
        time.sleep(DELAY)

    # 4. 逐渐变暗
    for duty_cycle in range(1023, -1, -8):
        led_pwm.duty(duty_cycle)  # 设置占空比
        time.sleep(DELAY)