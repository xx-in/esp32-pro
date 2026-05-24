class TM1637:
    """
    TM1637 4-Digit LED Display Driver
    """
    _CMD_DATA = 0x40  # Data command setting
    _CMD_ADDR = 0xC0  # Address command setting
    _CMD_DISP = 0x80  # Display control command

    # Segment map for 0-F
    _SEG_MAP = [
        0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07,
        0x7F, 0x6F, 0x77, 0x7C, 0x39, 0x5E, 0x79, 0x71
    ]

    def __init__(self, clk_pin, dio_pin, brightness=3):
        self.clk = machine.Pin(clk_pin, machine.Pin.OUT)
        self.dio = machine.Pin(dio_pin, machine.Pin.OUT)
        self._brightness = max(0, min(7, brightness))
        self._on = True
        self.clear()

    def _start(self):
        self.dio.init(machine.Pin.OUT, value=1)
        self.clk.init(machine.Pin.OUT, value=1)
        time.sleep_us(10)
        self.dio.value(0)
        time.sleep_us(10)
        self.clk.value(0)

    def _stop(self):
        self.dio.init(machine.Pin.OUT, value=0)
        time.sleep_us(10)
        self.clk.value(1)
        time.sleep_us(10)
        self.dio.value(1)

    def _write_byte(self, byte):
        # Send 8-bit data
        for _ in range(8):
            self.dio.value(byte & 0x01)
            time.sleep_us(10)
            self.clk.value(1)
            time.sleep_us(10)
            self.clk.value(0)
            byte >>= 1

        # Wait for Acknowledge (ACK)
        self.dio.init(machine.Pin.IN, machine.Pin.PULL_UP)
        time.sleep_us(10)
        self.clk.value(1)
        time.sleep_us(10)
        ack = self.dio.value()
        self.clk.value(0)
        self.dio.init(machine.Pin.OUT, value=0)
        return ack == 0

    def _write_command(self, cmd):
        self._start()
        self._write_byte(cmd)
        self._stop()

    def _update_display_control(self):
        # Brightness control: 0x80 (Display switch) | 0x08 (ON) | Brightness (0-7)
        cmd = self._CMD_DISP | (0x08 if self._on else 0x00) | self._brightness
        self._write_command(cmd)

    def show_time(self, hour, minute, show_colon=True):
        """Display time, e.g., 12:30"""
        h1, h2 = divmod(hour, 10)
        m1, m2 = divmod(minute, 10)
        
        segments = [
            self._SEG_MAP[h1],
            self._SEG_MAP[h2],
            self._SEG_MAP[m1],
            self._SEG_MAP[m2]
        ]
        
        # Handle colon (Highest bit of the 2nd digit controls the colon)
        if show_colon:
            segments[1] |= 0x80
            
        self._write_command(self._CMD_DATA)
        self._start()
        self._write_byte(self._CMD_ADDR)
        for seg in segments:
            self._write_byte(seg)
        self._stop()
        self._update_display_control()

    def clear(self):
        """Clear display"""
        self._write_command(self._CMD_DATA)
        self._start()
        self._write_byte(self._CMD_ADDR)
        for _ in range(4):
            self._write_byte(0x00)
        self._stop()
        self._update_display_control()
