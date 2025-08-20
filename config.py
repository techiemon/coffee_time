# Configuration file for Coffee Time Notification System
# Copy this file and rename to config.py, then fill in your credentials

# WiFi Configuration
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"

# Slack Configuration
SLACK_BOT_TOKEN = "xoxb-your-slack-bot-token-here"
SLACK_CHANNEL = "coffee"  # Channel name without #

# Hardware Configuration
BUTTON_PIN = 15  # GPIO pin for the button (adjust as needed)
LED_PIN = 25     # Built-in LED pin for status indication

# Timing Configuration (in seconds)
STALE_COFFEE_TIME = 7200  # 2 hours = 7200 seconds
DEBOUNCE_TIME = 0.05      # 50ms debounce
TRIPLE_PRESS_WINDOW = 2   # 2 seconds to detect triple press
