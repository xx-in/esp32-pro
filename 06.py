from machine import Pin

# 按键控制,开关连接在k1-k4四个接线上,这是输入

pin10 = Pin(10, Pin.IN, Pin.PULL_UP)  # 按键1
pin25 = Pin(25, Pin.OUT, Pin.PULL_UP)  # 继电器控制引脚
while True:
    if not pin10.value():  # 按键按下时，pin10的值为0
        print("按键1被按下了")
        pin25.on()  # 打开继电器
    else:
        print("按键1没有被按下")
        pin25.off()  # 关闭继电器


# 现在是按住检测，按住时继电器一直开着，松开时继电器关闭。可以根据需要调整代码实现不同的功能，比如按一次切换状态等。