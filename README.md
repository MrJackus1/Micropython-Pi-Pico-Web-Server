# Micropython-Pi-Pico-Projects
A place to put some little python Projects.
</br>
## Pi Pico Webserver
A webserver made with Micropython for Pi Pico W boards. It can handle requests and serve files over http. In the future i want to expand this into serveral servers such as ones for: http, https and a multithreaded server / versions of them.
#### Version 1
 - Basic file and folder support
 - Favicon support, please use small favicons as they stay loaded in the memory, this speeds up  the browser request for it.
 - http support
 - Easy to intergrate function support. Connect to your pico and use 'http:/your-pico-ip-here/pico', 'http://192.168.10.88/pico' for an example.
