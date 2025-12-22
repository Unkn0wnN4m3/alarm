import gc

import machine

# Free up memory early to maximize available heap for the main application
gc.collect()

# WiFi is intentionally not disabled here to allow faster connection in main.py
# Disabling would save ~30mA but add reconnection delay

print("System started")
print(f"Free memory: {gc.mem_free()} bytes")
