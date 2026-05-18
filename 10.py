from machine import Pin
import time

dc_motor = Pin(15, Pin.OUT, Pin.PULL_DOWN)

# in1 和 o1是相连的
# 边上那个5v的引脚是电源
# 之所以可以直接控制，使用使用驱动芯片，是因为电机的电压和电流都比较大，直接连接到单片机上会烧掉单片机，所以需要使用驱动芯片来控制电机的开关。
# ULN2003是一个常用的电机驱动芯片，可以控制直流电机的正反转和速度。它内部有四个H桥，可以同时控制四个直流电机或者一个步进电机。


if __name__ == "__main__":
    dc_motor.value(1)
    time.sleep(10)
    dc_motor.value(0)
