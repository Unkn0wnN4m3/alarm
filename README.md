# Alarm System for Raspberry Pi Pico W

Modular alarm system with magnetic sensor for windows, connected to Telegram with asynchronous architecture.

## Features

- 🔐 **Armed/disarmed system** via Telegram commands
- 📡 **Asynchronous monitoring** of magnetic sensor
- 🔔 **Instant notifications** when window opens
- 🛡️ **Whitelist** of authorized users
- ⚡ **Non-blocking operation** using asyncio
- 🏗️ **Modular architecture** with clean separation of concerns
- 🐛 **Debug mode** for development and testing
- 🔄 **Auto-recovery** with restart on failure (production mode)

## Required Hardware

- Raspberry Pi Pico W
- Magnetic door/window sensor (normally open)
- Connection wires

## Connections

```
Magnetic Sensor:
- Pin 1 → GPIO 16 (GP16) - configurable in config.py
- Pin 2 → GND

Onboard LED: Visual indicator (automatic on Pico W)
```

## Project Structure

```
alarm/
├── boot.py              # Boot initialization and memory management
├── main.py              # Main entry point and task orchestration
├── config.py            # Configuration file (created from config.example.py)
├── config.example.py    # Configuration template
└── lib/
    ├── commands.py      # Telegram command handlers
    ├── sensor.py        # Sensor monitoring logic
    ├── telegram.py      # Telegram bot API client
    └── wifi.py          # WiFi connection manager
```

## Configuration

### 1. Install MicroPython on Pico W

1. Download MicroPython firmware for Pico W from [micropython.org](https://micropython.org/download/RPI_PICO_W/)
2. Hold down the BOOTSEL button and connect Pico W to PC
3. Copy the `.uf2` file to the device

### 2. Create Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow the instructions

### 3. Configure the system

1. Copy the example configuration:
   ```bash
   cp config.example.py config.py
   ```

2. Edit `config.py` with your settings:

```python
# Set to False in production for automatic recovery
DEBUG_MODE = True

# WiFi credentials
WIFI_SSID = "YourWiFiNetwork"
WIFI_PASSWORD = "YourWiFiPassword"

# Telegram Bot
TELEGRAM_BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"

# Whitelist of authorized Chat IDs
WHITELIST_CHAT_IDS = [123456789, 987654321]

# Hardware configuration
SENSOR_PIN = 16  # GPIO 16 for magnetic sensor
LED_PIN = "LED"  # Pico W onboard LED
```

### 4. Upload the code

Use Thonny, mpremote or rshell to copy all files to Pico W:

```bash
# With mpremote (recommended)
mpremote cp boot.py main.py config.py :
mpremote mkdir lib
mpremote cp lib/commands.py lib/sensor.py lib/telegram.py lib/wifi.py :lib/

# Or copy entire lib folder
mpremote cp -r lib :

# With rshell
rshell -p COM3
> cp boot.py main.py config.py /pyboard/
> mkdir /pyboard/lib
> cp lib/*.py /pyboard/lib/
```

### 5. Run the system

The system will start automatically on boot. To run manually:

```bash
mpremote run main.py
```

## Usage

### Telegram Commands

- `/start` - Show available commands
- `/arm` - Arm the alarm system
- `/disarm` - Disarm the system
- `/status` - View current system and window status

### Operation

1. System starts disarmed
2. Use `/arm` to activate monitoring
3. When the window opens (magnetic sensor separates), you'll receive a notification
4. The onboard LED turns on while the window is open
5. Use `/disarm` to deactivate monitoring

## Architecture

The system uses a modular design with `uasyncio` for concurrent task execution:

### Core Components

- **`main.py`**: Entry point that orchestrates all components
- **`boot.py`**: Early initialization and memory optimization
- **`SensorManager`** (`lib/sensor.py`): Handles sensor monitoring and state management
- **`TelegramBot`** (`lib/telegram.py`): Telegram API client with async message handling
- **`process_command()`** (`lib/commands.py`): Command routing and execution
- **`connect_wifi()`** (`lib/wifi.py`): Async WiFi connection manager

### Concurrent Tasks

Two main tasks run simultaneously using `asyncio.gather()`:

1. **`sensor_manager.monitor()`**: Polls the magnetic sensor every 100ms
2. **`bot.run()`**: Handles Telegram API communication

Both tasks operate independently without blocking each other.

### Debug vs Production Mode

- **Debug Mode** (`DEBUG_MODE = True`):
  - Halts on fatal errors for mpremote debugging
  - Skips auto-restart to preserve system state
  - Allows manual code updates and inspection

- **Production Mode** (`DEBUG_MODE = False`):
  - Auto-restarts on WiFi failures (5s delay)
  - Auto-restarts on fatal errors (10s delay)
  - Ensures continuous operation

## Security

- Only users in `WHITELIST_CHAT_IDS` can control the system
- Other users will not receive a response from the bot
- Unauthorized access attempts are logged to console

## Troubleshooting

**Not connecting to WiFi:**
- Verify SSID and password
- Make sure to use 2.4GHz WiFi (Pico W doesn't support 5GHz)

**Not receiving Telegram messages:**
- Verify bot token
- Ensure Chat ID is in the whitelist
- Check internet connection

**Sensor not detecting changes:**
- Verify sensor connections
- Try reversing the sensor wires
- Use a multimeter to verify continuity

## Credits

This project uses the [micropython-telegram-bot](https://github.com/antirez/micropython-telegram-bot) library by Salvatore Sanfilippo ([@antirez](https://github.com/antirez)), licensed under BSD 2-Clause.

## Future Improvements

- Add multiple sensors
- Event history
- Silent mode with schedules
- Backup battery
- State persistence in flash
- Configuration via Telegram commands
