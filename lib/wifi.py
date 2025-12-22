import network
import uasyncio as asyncio


async def connect_wifi(ssid, password, timeout=10):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # Skip connection attempt if already connected from previous boot
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(ssid, password)
        
        # Async sleep allows other tasks to run during connection
        while not wlan.isconnected() and timeout > 0:
            await asyncio.sleep(1)
            timeout -= 1
        
        if wlan.isconnected():
            print(f"Connected: {wlan.ifconfig()}")
            return True
        else:
            print("Failed to connect to WiFi")
            return False
    return True
