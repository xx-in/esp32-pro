import machine
import time
import network
import ntptime
from tm1637 import TM1637
# ====================================================
# 1. TM1637 Display Driver Class
# ====================================================

# ====================================================
# 2. WiFi Connection Function
# ====================================================
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # WiFi status mapping
    status_map = {
        network.STAT_IDLE: "Idle/Uninitialized",
        network.STAT_CONNECTING: "Connecting...",
        network.STAT_WRONG_PASSWORD: "Failed: Wrong Password",
        network.STAT_NO_AP_FOUND: "Failed: SSID Not Found",
        network.STAT_CONNECT_FAIL: "Failed: Connection Error",
        network.STAT_GOT_IP: "Success: IP Obtained"
    }

    print(f"\n[WiFi] Attempting to connect to: {ssid}")
    
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        
        # Wait for connection, timeout after 20 seconds
        max_wait = 20
        while max_wait > 0:
            status = wlan.status()
            print(f"[WiFi] Status: {status_map.get(status, str(status))} (Remaining: {max_wait}s)")
            
            if wlan.isconnected():
                break
                
            time.sleep(1)
            max_wait -= 1

    if wlan.isconnected():
        ip_info = wlan.ifconfig()
        rssi = wlan.status('rssi')
        print("-" * 30)
        print(f"[WiFi] Connected successfully!")
        print(f"[WiFi] IP Address: {ip_info[0]}")
        print(f"[WiFi] Signal Strength: {rssi} dBm")
        print("-" * 30)
        return True
    else:
        print("[WiFi] Connection failed. Please check SSID or Password.")
        return False

# ====================================================
# 3. NTP Time Sync Function
# ====================================================
def sync_time():
    print("[NTP] 正在请求网络时间 (ntp.aliyun.com)...")
    ntptime.host = "ntp.aliyun.com"
    try:
        # 直接调用 settime，MicroPython 会使用默认的超时机制
        ntptime.settime()
        print("[NTP] 对时成功！")
        return True
    except Exception as e:
        # 如果还是报错，通常是网络连接问题或 DNS 解析失败
        print(f"[NTP] 对时失败: {e}")
        return False

# ====================================================
# 4. Main Program Logic
# ====================================================
def main():
    # --- Configuration ---
    WIFI_SSID = "ZTE-xDUdNN"
    WIFI_PASS = "2821550908"
    
    # Modify pins according to your wiring
    TM_CLK = 16 
    TM_DIO = 17
    
    # 1. Initialize Display
    tm = TM1637(clk_pin=TM_CLK, dio_pin=TM_DIO, brightness=3)
    tm.show_time(0, 0, True) # Initial display 00:00

    # 2. Connect WiFi
    if connect_wifi(WIFI_SSID, WIFI_PASS):
        # 3. Sync Network Time
        sync_time()
    else:
        print("[Warn] Continuing, but time may be inaccurate.")

    print("[System] Real-Time Clock started...")
    
    last_second = -1
    
    try:
        while True:
            # Get UTC timestamp and convert to UTC+8 (Beijing Time)
            beijing_time = time.time() + 8 * 3600
            t = time.localtime(beijing_time)
            hour = t[3]      # Hour
            minute = t[4]    # Minute
            second = t[5]    # Second
            
            # Refresh display every second
            if second != last_second:
                # Colon blinking logic: ON for even seconds, OFF for odd seconds
                show_colon = (second % 2 == 0)
                tm.show_time(hour, minute, show_colon)
                
                # Serial debug output
                # print(f"Current Time: {hour:02d}:{minute:02d}:{second:02d}")
                
                last_second = second
            
            # Loop slightly faster than 1s to ensure smooth blinking
            time.sleep(0.2)
            
    except KeyboardInterrupt:
        print("\n[System] Program stopped by user")
        tm.clear()

if __name__ == "__main__":
    main()