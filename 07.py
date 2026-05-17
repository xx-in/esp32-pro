from machine import Pin
import time

# 1. 初始化引脚
pin10 = Pin(10, Pin.IN, Pin.PULL_UP)  # 按键1
pin25 = Pin(25, Pin.OUT)              # 继电器控制引脚

# 确保初始状态继电器是关闭的
pin25.off()

# 记录上一次变化的时间，用于软件消抖
last_trigger_time = 0

# 2. 中断服务函数 (ISR)
def button_handler(p):
    global last_trigger_time
    
    current_time = time.ticks_ms()
    
    # 软件消抖：限制两次电平变化触发的间隔不能小于 20 毫秒
    if time.ticks_diff(current_time, last_trigger_time) > 20:
        
        # 判断当前引脚状态
        if p.value() == 0:  
            # 电平为 0，说明按键被【按住】了
            print("按键1被按下了 -> 开启继电器")
            pin25.on()
        else:               
            # 电平为 1，说明按键被【松开】了
            print("按键1没有被按下 -> 关闭继电器")
            pin25.off()
            
        # 更新时间戳
        last_trigger_time = current_time

# 3. 配置配置中断映射
# Pin.IRQ_FALLING（下降沿 = 按下） | Pin.IRQ_RISING（上升沿 = 松开）
# 不管按下还是松开，都会实时触发 button_handler 函数
pin10.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=button_handler)

# 4. 主循环完全释放
while True:
    # 主循环现在不需要做任何按键检测，可以用来做别的事或者休眠
    time.sleep(1)