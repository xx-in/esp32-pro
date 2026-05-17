from machine import Pin
import time

# 按键控制, 开关连接在k1接线上, 这是输入
pin10 = Pin(10, Pin.IN, Pin.PULL_UP)  # 按键1
pin25 = Pin(25, Pin.OUT)              # 继电器控制引脚（输出通常不需要设置 PULL_UP）

# 按一次切换状态
state = False  # 初始状态为关闭
pin25.off()   # 确保初始状态继电器关闭

while True:
    # 1. 检测按键是否按下
    if not pin10.value():  
        time.sleep_ms(20)  # 软件消抖：等待20毫秒，避开机械抖动
        
        # 2. 再次确认是否真的按下
        if not pin10.value():  
            print("按键1被按下了")
            state = not state  # 切换状态
            
            # 改变继电器状态
            if state:
                pin25.on()     # 打开继电器
            else:
                pin25.off()    # 关闭继电器
            
            # 3. 死循环等待按键松开：只要按键还按着（值是0），就卡在这里不动
            # 这样就能完美维持住状态，直到你松开手，才会等待下一次按下
            while not pin10.value():
                time.sleep_ms(10)  # 稍微延时，释放一点CPU资源