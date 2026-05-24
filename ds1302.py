from machine import Pin
import time

class DS1302:
    def __init__(self, clk, dio, cs):
        self.clk = Pin(clk, Pin.OUT)
        self.dio = Pin(dio, Pin.OUT)
        self.cs = Pin(cs, Pin.OUT)
        self.cs.value(0); self.clk.value(0)

    def _dec2bcd(self, dec):
        return (dec // 10) << 4 | (dec % 10)

    def _bcd2dec(self, bcd):
        return (bcd >> 4) * 10 + (bcd & 0x0F)

    def _write_byte(self, dat):
        self.dio.init(Pin.OUT)
        for i in range(8):
            self.dio.value((dat >> i) & 1)
            time.sleep_us(10) # 延迟：确保 DS1302 能读到电平
            self.clk.value(1)
            time.sleep_us(10) # 延迟：稳定高电平
            self.clk.value(0)

    def _read_byte(self):
        self.dio.init(Pin.IN)
        dat = 0
        for i in range(8):
            bit = self.dio.value()
            dat |= (bit << i)
            self.clk.value(1)
            time.sleep_us(10) # 延迟
            self.clk.value(0)
            time.sleep_us(10) # 延迟
        return dat

    def date_time(self, dt=None):
        if dt is None:
            # 读取时间
            self.cs.value(1)
            self._write_byte(0xBF) # 突发读取模式
            res = [self._bcd2dec(self._read_byte()) for _ in range(7)]
            self.cs.value(0)
            # 返回: [年, 月, 日, 星期, 时, 分, 秒]
            return [res[6], res[4], res[3], res[5], res[2], res[1], res[0]]
        else:
            # 写入时间 dt: [YY, MM, DD, Week, hh, mm, ss]
            self.cs.value(1)
            self._write_byte(0x8E); self._write_byte(0) # 解除写保护
            self.cs.value(0)
            
            self.cs.value(1)
            self._write_byte(0xBE) # 突发写入模式
            self._write_byte(self._dec2bcd(dt[6])) # 秒
            self._write_byte(self._dec2bcd(dt[5])) # 分
            self._write_byte(self._dec2bcd(dt[4])) # 时
            self._write_byte(self._dec2bcd(dt[2])) # 日
            self._write_byte(self._dec2bcd(dt[1])) # 月
            self._write_byte(self._dec2bcd(dt[3])) # 星期
            self._write_byte(self._dec2bcd(dt[0])) # 年
            self._write_byte(0) # 再次写保护
            self.cs.value(0)