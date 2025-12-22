import uasyncio as asyncio
from machine import Pin


class SensorManager:
    def __init__(self, sensor_pin, led_pin, notify_callback):
        # PULL_DOWN ensures stable LOW when sensor is closed (contacts together)
        self.sensor = Pin(sensor_pin, Pin.IN, Pin.PULL_UP)
        self.led = Pin(led_pin, Pin.OUT)
        # Store initial state to detect changes rather than absolute values
        self.last_state = self.sensor.value()
        self.system_armed = False
        self.notify_callback = notify_callback

    def arm(self):
        self.system_armed = True

    def disarm(self):
        self.system_armed = False
        # Turn off LED since visual alert is no longer needed
        self.led.off()

    def is_armed(self):
        return self.system_armed

    def window_state(self):
        return "OPEN" if self.sensor.value() == 1 else "CLOSED"

    async def monitor(self):
        while True:
            current_state = self.sensor.value()

            # Only trigger notifications on state changes to avoid spam
            if self.system_armed and current_state != self.last_state:
                if current_state == 1:
                    print("ALERT! Window open")
                    self.led.on()
                    await self.notify_callback("⚠️ ALERT: Window opened detected!")
                else:
                    print("Window closed")
                    self.led.off()

            self.last_state = current_state
            # 100ms polling is fast enough for human-triggered events while keeping CPU usage low
            await asyncio.sleep(0.1)
