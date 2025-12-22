# config.example.py
# Copy this file to config.py and configure your credentials

# Set to False in production for automatic recovery
DEBUG_MODE = True

# WiFi
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"

# Telegram Bot
TELEGRAM_BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"

# Whitelist of authorized Chat IDs
# To get your Chat ID:
# 1. Send a message to your bot
# 2. Visit: https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
# 3. Look for the "id" field inside "chat"
WHITELIST_CHAT_IDS = [123456789, 987654321]

# Hardware configuration
SENSOR_PIN = 16  # GPIO 16 for magnetic sensor
LED_PIN = "LED"  # Pico W onboard LED
