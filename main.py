"""
Coffee Time Notification System for RP2350 Pico W5
Sends Slack notifications when coffee is ready or stale
"""

import machine
import network
import urequests
import ujson
import time
import _thread
from coffee_quotes import get_random_quote
from config import (
    WIFI_SSID, WIFI_PASSWORD, SLACK_BOT_TOKEN, SLACK_CHANNEL,
    BUTTON_PIN, LED_PIN, STALE_COFFEE_TIME, DEBOUNCE_TIME, TRIPLE_PRESS_WINDOW
)

class CoffeeNotifier:
    def __init__(self):
        # Hardware setup
        self.button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)
        self.led = machine.Pin(LED_PIN, machine.Pin.OUT)
        
        # State variables
        self.wifi_connected = False
        self.last_coffee_time = 0
        self.stale_timer_active = False
        self.button_presses = []
        self.last_button_state = 1
        
        # Slack API endpoint
        self.slack_url = "https://slack.com/api/chat.postMessage"
        
        print("Coffee Time Notification System Starting...")
        self.led.on()  # LED on during startup
        
    def connect_wifi(self):
        """Connect to WiFi network"""
        print(f"Connecting to WiFi: {WIFI_SSID}")
        
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        # Wait for connection
        max_wait = 10
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            max_wait -= 1
            print('Waiting for connection...')
            time.sleep(1)
            
        if wlan.status() != 3:
            print('Network connection failed')
            self.blink_error()
            return False
        else:
            print('Connected to WiFi')
            print('IP:', wlan.ifconfig()[0])
            self.wifi_connected = True
            return True
            
    def blink_error(self):
        """Blink LED to indicate error"""
        for _ in range(10):
            self.led.on()
            time.sleep(0.1)
            self.led.off()
            time.sleep(0.1)
            
    def send_slack_message(self, message):
        """Send message to Slack channel"""
        if not self.wifi_connected:
            print("WiFi not connected, cannot send message")
            return False
            
        headers = {
            'Authorization': f'Bearer {SLACK_BOT_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'channel': SLACK_CHANNEL,
            'text': message,
            'username': 'Coffee Bot',
            'icon_emoji': ':coffee:'
        }
        
        try:
            print(f"Sending to Slack: {message}")
            response = urequests.post(
                self.slack_url,
                headers=headers,
                data=ujson.dumps(data)
            )
            
            if response.status_code == 200:
                result = ujson.loads(response.text)
                if result.get('ok'):
                    print("Message sent successfully!")
                    self.flash_success()
                    return True
                else:
                    print(f"Slack API error: {result.get('error', 'Unknown error')}")
            else:
                print(f"HTTP error: {response.status_code}")
                
            response.close()
            
        except Exception as e:
            print(f"Error sending message: {e}")
            
        self.blink_error()
        return False
        
    def flash_success(self):
        """Flash LED to indicate success"""
        for _ in range(3):
            self.led.off()
            time.sleep(0.2)
            self.led.on()
            time.sleep(0.2)
            
    def check_button_press(self):
        """Check for button press with debouncing"""
        current_state = self.button.value()
        
        # Button pressed (falling edge)
        if self.last_button_state == 1 and current_state == 0:
            time.sleep(DEBOUNCE_TIME)  # Debounce
            if self.button.value() == 0:  # Confirm press
                current_time = time.time()
                self.button_presses.append(current_time)
                
                # Remove old presses outside the triple-press window
                self.button_presses = [
                    press_time for press_time in self.button_presses
                    if current_time - press_time <= TRIPLE_PRESS_WINDOW
                ]
                
                print(f"Button pressed! ({len(self.button_presses)} presses in window)")
                
                # Check for triple press
                if len(self.button_presses) >= 3:
                    self.handle_triple_press()
                    self.button_presses = []  # Reset after triple press
                else:
                    # Single press - start timer for potential triple press
                    _thread.start_new_thread(self.handle_single_press_delayed, ())
                    
        self.last_button_state = current_state
        
    def handle_single_press_delayed(self):
        """Handle single press after waiting for potential triple press"""
        time.sleep(TRIPLE_PRESS_WINDOW + 0.1)  # Wait a bit longer than window
        
        # If we still have fewer than 3 presses, treat as single press
        if len(self.button_presses) < 3 and len(self.button_presses) > 0:
            self.handle_single_press()
            self.button_presses = []
            
    def handle_single_press(self):
        """Handle single button press - fresh coffee notification"""
        print("Single press detected - Fresh coffee!")
        
        message = "Move your feet, fresh coffee is on! ☕"
        if self.send_slack_message(message):
            self.last_coffee_time = time.time()
            self.start_stale_timer()
            
    def handle_triple_press(self):
        """Handle triple button press - random coffee quote"""
        print("Triple press detected - Sending random coffee quote!")
        
        quote = get_random_quote()
        message = f"☕ Coffee Wisdom: {quote}"
        self.send_slack_message(message)
        
    def start_stale_timer(self):
        """Start timer for stale coffee notification"""
        if self.stale_timer_active:
            return  # Timer already running
            
        self.stale_timer_active = True
        _thread.start_new_thread(self.stale_coffee_timer, ())
        
    def stale_coffee_timer(self):
        """Timer thread for stale coffee notification"""
        print(f"Starting stale coffee timer ({STALE_COFFEE_TIME} seconds)")
        
        start_time = time.time()
        while time.time() - start_time < STALE_COFFEE_TIME:
            time.sleep(1)
            
            # Check if fresh coffee was made (reset timer)
            if self.last_coffee_time > start_time:
                print("Fresh coffee detected, resetting stale timer")
                self.stale_timer_active = False
                self.start_stale_timer()  # Restart with new time
                return
                
        # Timer expired - send stale coffee message
        print("Coffee is now stale!")
        message = "Help, coffee is cold or gone by now. ❄️☕"
        self.send_slack_message(message)
        self.stale_timer_active = False
        
    def run(self):
        """Main application loop"""
        # Connect to WiFi
        if not self.connect_wifi():
            print("Failed to connect to WiFi. Check your credentials.")
            return
            
        self.led.off()  # Turn off LED after successful startup
        print("Coffee Time System Ready! Press the button to notify about fresh coffee.")
        print("Triple-press for a random coffee quote.")
        
        # Main loop
        while True:
            try:
                self.check_button_press()
                time.sleep(0.01)  # Small delay to prevent excessive CPU usage
                
            except KeyboardInterrupt:
                print("\nShutting down Coffee Time System...")
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                self.blink_error()
                time.sleep(1)

# Create and run the coffee notifier
if __name__ == "__main__":
    try:
        notifier = CoffeeNotifier()
        notifier.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        # Blink LED rapidly to indicate fatal error
        led = machine.Pin(LED_PIN, machine.Pin.OUT)
        for _ in range(20):
            led.on()
            time.sleep(0.05)
            led.off()
            time.sleep(0.05)
