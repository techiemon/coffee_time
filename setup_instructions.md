# Coffee Time Notification System Setup Instructions

## Hardware Requirements
- RP2350 Pico W5 Board with 2.4GHz/5.8GHz WiFi Support
- Push button
- Breadboard and jumper wires
- MicroUSB cable

## Hardware Setup

### Button Connection
1. Connect one side of the button to GPIO pin 15 (configurable in `config.py`)
2. Connect the other side of the button to GND
3. The internal pull-up resistor is enabled in software

### LED Indicator
- The built-in LED (GPIO 25) is used for status indication:
  - **Solid ON**: System starting up
  - **OFF**: System ready and operational
  - **3 quick flashes**: Message sent successfully
  - **10 rapid blinks**: Error occurred

## Software Setup

### 1. Install MicroPython
1. Download the latest MicroPython firmware for RP2350 from [micropython.org](https://micropython.org/download/)
2. Hold the BOOTSEL button while connecting the Pico to your computer
3. Copy the `.uf2` firmware file to the RPI-RP2 drive that appears
4. The Pico will reboot and appear as a serial device

### 2. Upload Files
Copy these files to your Pico W5:
- `main.py` - Main application
- `config.py` - Configuration file
- `coffee_quotes.py` - Coffee quotes database

### 3. Configure Settings
Edit `config.py` with your specific settings:

```python
# WiFi Configuration
WIFI_SSID = "YourWiFiNetwork"
WIFI_PASSWORD = "YourWiFiPassword"

# Slack Configuration
SLACK_BOT_TOKEN = "xoxb-your-actual-bot-token"
SLACK_CHANNEL = "coffee"  # Your channel name

# Hardware Configuration (adjust if needed)
BUTTON_PIN = 15  # GPIO pin for button
LED_PIN = 25     # Built-in LED

# Timing Configuration
STALE_COFFEE_TIME = 7200  # 2 hours in seconds
```

## Slack Bot Setup

### 1. Create a Slack App
1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click "Create New App" → "From scratch"
3. Name your app (e.g., "Coffee Bot") and select your workspace

### 2. Configure Bot Permissions
1. Go to "OAuth & Permissions" in your app settings
2. Add these Bot Token Scopes:
   - `chat:write` - Send messages
   - `chat:write.public` - Send messages to public channels
3. Install the app to your workspace
4. Copy the "Bot User OAuth Token" (starts with `xoxb-`)

### 3. Add Bot to Channel
1. Go to your #coffee channel in Slack
2. Type `/invite @CoffeeBot` (or your bot's name)
3. The bot should now be able to post messages

## Usage

### Single Button Press
- **Action**: Press and release the button once
- **Result**: Sends "Move your feet, fresh coffee is on! ☕" to Slack
- **Timer**: Starts a 2-hour countdown for stale coffee notification

### Triple Button Press
- **Action**: Press the button 3 times quickly (within 2 seconds)
- **Result**: Sends a random coffee quote to Slack
- **Examples**: 
  - "May your coffee be strong and your Monday be short."
  - "Coffee helps me maintain my 'never killed anyone streak.'"

### Automatic Stale Coffee Alert
- **Trigger**: 2 hours after the last fresh coffee notification
- **Message**: "Help, coffee is cold or gone by now. ❄️☕"
- **Reset**: Making fresh coffee resets the timer

## Troubleshooting

### WiFi Connection Issues
- Check SSID and password in `config.py`
- Ensure your WiFi network is 2.4GHz (5GHz may not work)
- LED will blink rapidly if WiFi connection fails

### Slack Message Issues
- Verify your bot token is correct and starts with `xoxb-`
- Ensure the bot has been added to the target channel
- Check that the channel name in config matches exactly (no # symbol)

### Button Not Responding
- Check button wiring (one side to GPIO 15, other to GND)
- Verify the button pin number in `config.py`
- Try a different GPIO pin if needed

### System Errors
- Connect to the Pico via serial console to see error messages
- LED will blink rapidly (10 times) when errors occur
- Check the serial output for detailed error information

## Customization

### Changing Button Pin
Edit `BUTTON_PIN` in `config.py` to use a different GPIO pin.

### Adjusting Stale Coffee Time
Modify `STALE_COFFEE_TIME` in `config.py` (value in seconds):
- 1 hour: 3600
- 2 hours: 7200 (default)
- 3 hours: 10800

### Adding More Quotes
Edit `coffee_quotes.py` and add new quotes to the `COFFEE_QUOTES` list.

### Custom Messages
Modify the message strings in `main.py`:
- Fresh coffee: Line ~140
- Stale coffee: Line ~180
- Random quote: Line ~150

## File Structure
```
coffee_time/
├── main.py              # Main application
├── config.py            # Configuration settings
├── coffee_quotes.py     # Coffee quotes database
├── setup_instructions.md # This file
└── Readme.md           # Project description
```

## Support
If you encounter issues:
1. Check the serial console output for error messages
2. Verify all connections and configuration settings
3. Ensure your Slack bot has proper permissions
4. Test WiFi connectivity separately if needed
