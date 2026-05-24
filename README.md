## 创建环境
```sh
uv venv
```

## 安装依赖

`mpremote` 是一个控制工具，可以操作基于 `micropython` 的单片机。

```sh
uv add mpremote
```

## 启动命令
```
mpremote run [name].py
```

## 实验内容

- 01.py 开灯
- 02.py 单灯闪烁
- 03.py 跑马灯闪烁
- 04.py 蜂鸣器
- 05.py 继电器
- 06.py 按键长按触发
- 07.py 按键长按触发 - 中断模式
- 08.py 按键点击切换
- 09.py 按键点击切换 - 中断模式
- 10.py 直流电机控制
- 11.py 定时器中断
- 12.py pwm调光
- 13.py rgb灯爆闪
- 14.py 关闭灯
- 15.py 连接wifi后显示时间


## 注意事项

- mpremote 在windows中对中文支持很差
- ds1302芯片供电需要是5v，但默认接的3.3v基本读不到有用数据
- 对于wifi，连接后会自动重连
- 对于芯片重置问题，按住boot键