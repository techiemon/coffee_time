I need an application for the RP2350 Pico W5 Board with 2.4GHz/5.8GHz Wifi Support

Spec sheet is here: https://www.elecrow.com/wiki/PICO_W5_RP2040_Dev_Board.html

The Micropython application will have a GPIO pin assigned to a button. 

When the button is pressed it will make an API call to the Slack API with an API key to post a message to a company slack channel called "coffee"

Config options to compile the firmware:

Wifi SSID and Password
Slack API key
Time_To_Stale

When the button is pressed the message 
"Move your feet, fresh coffee is on!"

Then start a timer, if after 2 hours no one has pressed the button again send. 
"Help, coffee is cold or gone by now."

At any time press the button 3 times quickly to send out a random quote about coffee.   Help me research and come up a long list of quotes or jokes about coffee.