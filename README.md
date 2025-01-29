# Micropython Pi Pico Web Server
Welcome to yet another Pi Pico Web Server.
</br>
## Pi Pico Webserver
A webserver made with Micropython for Pi Pico W boards. It can handle requests and serve: files, .js, .css, etc over http. In the future i want to expand this into serveral servers such as ones for: http, https and a multithreaded server / versions of them.
## How to install and run Pi Pico Webserver
- Open web_server.ini in notepad and edit the contents with your setup requirements. SD card doesnt have to be filled out if set to false. SDcard support is optional. If you want to use it please download 'sdcard.py' from the repository below. And edit the .ini so that sdcard is set to true and you tell the server what pins it is connected to.
-  Copy 'Pico_Webserver_v1.2.py', 'update_rtc_time.py', 'web_server.ini' and 'your_website_folder' to the root of your Pico W. If using an sdcard only 'your_website_folder' is on the sd.
-  Run 'Pico_Webserver_1.2.py', change to 'main.py' if you want to run on start.
#### Version 1.2
 - Auto update RTC on Wifi Connect.
 - SD Card support via the 'sdcard.py'. -- https://github.com/micropython/micropython-lib/tree/master/micropython/drivers/storage/sdcard
 - Updated web_server.ini
 - More graceful error handling.
 - https support soon...
#### Version 1.1
 - Settings.ini support. Now allows the user to add their Wifi and webserver settings without having to change the pico_webserver.py (Allows the program to be used with mpy-cross!)
 - Added in some garbage collection.
 - Set WIFI powermode to full power. Improves request response times massively! (Maybe will be a setting in the ini soon. Trades power usage of the WIFI chip for improved networking capability.)
#### Version 1
 - Basic file and folder support
 - Favicon support, please use small favicons as they stay loaded in the memory, this speeds up  the browser request for it.
 - http support
 - Easy to intergrate function support. Connect to your pico and use 'http:/your-pico-ip-here/pico', 'http://192.168.10.88/pico' for an example.
