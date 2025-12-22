def process_command(bot, sensor_manager, chat_id, text):
    # Case-insensitive matching for user convenience
    text = text.lower()

    if text == "/start":
        bot.send(
            chat_id,
            "Welcome to the alarm system\n"
            "/arm - Arm the system\n"
            "/disarm - Disarm the system\n"
            "/status - View current status",
        )

    elif text == "/arm":
        sensor_manager.arm()
        bot.send(chat_id, "✅ System armed")
        # Console log for debugging without checking Telegram
        print("System armed")

    elif text == "/disarm":
        sensor_manager.disarm()
        bot.send(chat_id, "🔓 System disarmed")
        print("System disarmed")

    elif text == "/status":
        status = "ARMED" if sensor_manager.is_armed() else "DISARMED"
        window = sensor_manager.window_state()
        bot.send(
            chat_id, f"📊 System status:\nSystem: {status}\nWindow: {window}"
        )
