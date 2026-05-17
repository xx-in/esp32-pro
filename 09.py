from machine import Pin
import time

# 1. 初始化引脚
pin10 = Pin(10, Pin.IN, Pin.PULL_UP)  # 按键1
pin25 = Pin(25, Pin.OUT)              # 继电器控制引脚

# 2. 全局状态变量
state = False
pin25.off()  # 初始关闭继电器

# 记录上一次成功触发的时间，用于软件消抖
last_trigger_time = 0

# 3. 中断服务函数 (ISR)
# 当按键按下时，微控制器会自动调用这个函数。注意：中断函数必须带有一个参数（通常命名为 p），代表触发中断的 Pin 对象。
def button_handler(p):
    global state, last_trigger_time
    
    current_time = time.ticks_ms()
    
    # 软件消抖：判断当前时间与上一次触发时间是否大于 200 毫秒
    # 如果两次中断间隔太短，说明是机械抖动，直接忽略
    if time.ticks_diff(current_time, last_trigger_time) > 200:
        print("按键1触发了中断")
        state = not state  # 切换状态
        
        if state:
            pin25.on()     # 打开继电器
        else:
            pin25.off()    # 关闭继电器
            
        # 更新上一次触发的时间
        last_trigger_time = current_time

# 4. 配置配置中断映射
# trigger=Pin.IRQ_FALLING 表示在引脚电平“下降沿”（即由高变低，也就是按键按下的瞬间）触发中断
# handler=button_handler 指定触发后执行哪个函数
pin10.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)

# 5. 主循环现在完全释放了！
# 你可以在这里让芯片休眠，或者执行其他复杂的任务，完全不影响按键的响应
while True:
    time.sleep(1)  # 模拟主循环在做别的事情，或者单纯休眠节能