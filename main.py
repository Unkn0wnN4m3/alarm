import machine
import uasyncio as asyncio

from config import (
    DEBUG_MODE,
    LED_PIN,
    SENSOR_PIN,
    TELEGRAM_BOT_TOKEN,
    WHITELIST_CHAT_IDS,
    WIFI_PASSWORD,
    WIFI_SSID,
)
from lib.commands import process_command
from lib.sensor import SensorManager
from lib.telegram import TelegramBot
from lib.wifi import connect_wifi

# Globals needed because telegram_callback is synchronous but needs access to these instances
bot = None
sensor_manager = None


async def notify_alert(message):
    for chat_id in WHITELIST_CHAT_IDS:
        bot.send(chat_id, message)


def telegram_callback(
    bot_instance, msg_type, chat_name, sender_name, chat_id, text, entry
):
    # Security boundary: reject unauthorized users early
    if chat_id not in WHITELIST_CHAT_IDS:
        print(f"Access denied for chat_id: {chat_id}")
        return

    process_command(bot_instance, sensor_manager, chat_id, text)


async def main():
    global bot, sensor_manager

    print("Starting alarm system...")
    print(f"Debug mode: {DEBUG_MODE}")

    # WiFi must be established before Telegram API calls
    if not await connect_wifi(WIFI_SSID, WIFI_PASSWORD):
        print("Could not connect to WiFi.")
        if DEBUG_MODE:
            print("Stopping to allow manual intervention via mpremote...")
            return
        else:
            print("Restarting in 5 seconds...")
            await asyncio.sleep(5)
            machine.reset()

    bot = TelegramBot(TELEGRAM_BOT_TOKEN, telegram_callback)

    sensor_manager = SensorManager(SENSOR_PIN, LED_PIN, notify_alert)

    # Brief LED flash confirms successful initialization
    print("System ready")
    sensor_manager.led.on()
    await asyncio.sleep(0.5)
    sensor_manager.led.off()

    sensor_task = asyncio.create_task(sensor_manager.monitor())
    bot_task = asyncio.create_task(bot.run())

    # gather ensures both tasks run until one fails or is cancelled
    await asyncio.gather(sensor_task, bot_task)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("System stopped")
except Exception as e:
    print(f"Fatal error: {e}")
    if DEBUG_MODE:
        # Halt to allow mpremote access for debugging and code updates
        print("System halted. Use mpremote to update or press CTRL+D to restart REPL.")
    else:
        # In production, try to recover by restarting after a delay
        print("System will restart in 10 seconds...")
        import time

        time.sleep(10)
        machine.reset()
