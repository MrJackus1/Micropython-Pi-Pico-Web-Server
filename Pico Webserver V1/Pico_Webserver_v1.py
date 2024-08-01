# This program has turned into a webserver for a pi pico using Micropython and stock libs. 
'''
    This is my Pico W webserver V1

    ToDo:
        - Create a settings file and a way to autoload on startup and check all the values are inputted correctly.
        - Check that a normal website will work, folders ect. Only files are confirmed atm. But it should work?!?!?



'''
# Import modules here
import network, socket, machine, sys, time, os
from machine import Pin, ADC

# WIFI Credentials
sid = ''
passwd = ''

# Webserver Port, default ip should be 0.0.0.0 to avoid errors in reconnecting.
port = 80
server_ip = '0.0.0.0'
working_folder = 'web_server'

# Globar Vars
network_info = []
led = Pin('LED', Pin.OUT)
start_time = time.time()

# Functions
def load_favicon(filename='favicon.ico', path=''):
    x = path + filename
    if x in os.listdir():
        print('Favicon loaded.')
        with open(x, 'rb') as f:
            return f.read()
    else:
        print('No Favicon.')
        return 0

def get_temp():
    sensor = ADC(4)
    Conv = 3.3 / 65535
    v = sensor.read_u16()
    v = v * Conv
    Temp = round((27 - (v - 0.706) / 0.001721),1)
    return str(f"{Temp}C")

def set_led():
    led.toggle()
    x = led.value()
    if x == 0:
        return 'LED off.'
    elif x == 1:
        return 'LED on.'
    else: 
        return 'LED Error'

def set_darkmode():
    darkmode = ''
    current_time = time.localtime()
    hour = current_time[3]
    # Dark between 6pm and 6am
    if hour > 17 or hour < 7:
        darkmode = 'dark'
    else:
        darkmode = 'light'
    print(f'Darkmode set to: {darkmode}')
    return darkmode

def webpage(starttime):
    darkmode = set_darkmode()
    cpu_temp = get_temp()
    led_state = set_led()
    uptime = time.time() - starttime
    page = r"""
    <!DOCTYPE html>
    <html lang='en' data-theme='%s'>
    <head>
        <title>Pico Webserver!</title>
        <meta name='viewport' content='width=device-width, initial-scale=1'>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">

    </head>
    <body>
        <header class='container text-center'>
            <h1>Pico Webserver V1</h1>
            <p>Welcome to my Pi Pico webserver!</p>
            <nav>
            <ul>
                <li><strong>Pi Pico Server</strong></li>
            </ul>
            <ul>
                <li>
                <details class="dropdown">
                    <summary>
                    Dark / Light Mode
                    </summary>
                    <ul dir="rtl">
                    <li><a href="#" id='light_btn' >Light</a></li>
                    <li><a href="#" id='dark_btn' >Dark</a></li>
                    </ul>
                </details>
                </li>
            </ul>
            </nav>
        </header>
            <main class="container">
        <h2>Pi Pico Output</h1>
        <table class='striped'>
            <thead>
                <tr>
                    <th>Function</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>CPU Temp</td>
                    <td>%s</td>
                </tr>
                <tr>
                    <td>LED State</td>
                    <td>%s</td>
                </tr>
                <tr>
                    <td>Server Up Time</td>
                    <td>%s</td>
            </tbody>
        </table>
    </main>
    </body>
    <script>
        document.getElementById('light_btn').onclick = function() {changeMode('light')};
        document.getElementById('dark_btn').onclick = function() {changeMode('dark')};
        
        function changeMode(mode){
            var htmlTag = document.documentElement;
            htmlTag.setAttribute('data-theme', mode);
            console.log('New theme set:', mode)
        }
    </script>
    </html>
    """ % (darkmode, cpu_temp, led_state, uptime)
    return page

def connect_to_wifi(name='', password=''):
    global network_info
    try:
        class ConnectionError(Exception):
            pass
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.config(pm = 0xa11140)
        wlan.connect(ssid=sid, key=passwd)
        print(f'Connecting to {sid}, please wait.')
        timeout = 5
        while not wlan.isconnected():
            if timeout > 0:
                time.sleep(1)
                print(f'Connecting... {timeout}')
                timeout -= 1
            elif timeout == 0:
                print('Connection failed.')
                raise ConnectionError(f'WIFI connection to {sid} failed. Connection timed out. \nWLAN-Status: {wlan.status()}')
        time.sleep(1)
        if wlan.status() == 3:
            network_info = wlan.ifconfig()
            print(f'Connected to: {sid}  :  WLAN-Status: {wlan.status()}  :  IP Address: {network_info[0]}')
        else:
            raise ConnectionError(f'WIFI connection to {sid} failed. \nWLAN-Status: {wlan.status()}')
            sys.exit()
    except ConnectionError as ce:
        print(f'ConnectionError: {ce}')
        sys.exit()

def open_file(filename='', path=''):
    filename = '/' + path + '/' + filename
    if (path.replace('/', '')) or filename in os.listdir():
        with open(filename, 'r') as file:
            print('File loaded.')
            return file.read()
    else:
        print(f'Error: File does not exist: {filename}')
        return '404 - Page Not Found.'

def start_webserver(starttime, working_dir):
    opn_file = open_file
    website = webpage
    favicon = load_favicon()
    all_files = os.listdir(working_dir)
    # Create and open a socket for listening for incomming connections.
    addr = socket.getaddrinfo(server_ip, port)[0][-1]    
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(addr)
    sock.listen(3)
    print(f'Server is running on: {network_info[0]}, listening to {addr}')

    # Create a loop to listen for connections
    while True:
        try:
            client, address = sock.accept()
            print(f'Connection received from: {address}')            
            # Receive the request from client.
            client.settimeout(10)
            request = client.recv(1024)
            # This will ignore any empty requests from clients.
            if not request:
                raise OSError('Ignoring Request. Received empty request.')
            request = str(request)
            print(f'Request content: {request}')

            # This is where you can process a request...
            try:
                request = request.split()[1]
                print('Request:', request)
            except IndexError:
                pass
            if request == b'':
                raise OSError('Received empty request.')
            elif request == '/pico':
                response = website(starttime)
            elif request == '/': # Send the index of the site here. index.html 
                client.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                response = opn_file('index.html', working_dir)
            elif request =='/favicon.ico':
                print('Favicon requested.')
                client.send('HTTP/1.1 200 OK\r\nContent-Type: image/x-icon\r\n\r\n')
                response = favicon
            else:
                try:
                    request = request.strip('/')
                    response = opn_file(request, working_dir)
                    client.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                except IndexError as i:
                    print(f'Error: {i}')
                except OSError as ose:
                    print(f'Error File doesnt exist: {ose}')
                    response = '404 - Error, Page not found!' 

            # Send the http response and close the connection.
            client.send(response)
            client.close()
        except OSError as ose:
            print(f'Error: {ose}')
            client.close()
        except KeyboardInterrupt as ki:
            print(f'Error KeyboardInterrupt: {ki}')
            try:
                client.close()
                print('Keyboard Interrupt: server stopping.')
                sys.exit()
            except NameError:
                pass
            sys.exit()

# Code
connect_to_wifi()
start_webserver(start_time, working_folder)
print('Server stopped.')
sys.exit()