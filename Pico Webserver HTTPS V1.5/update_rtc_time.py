# This program will send a http request, parse the response and try to set the RTC on the pi pico using Micropython.
# It has a little failover if the first url fails.

import urequests, time, machine, sys

# Functions
def load_ini_file(filename):  
    class settings_dict(dict):
        # Init function
        def __init__(self):
            self = dict()
        # Add key pair here
        def join(self, key, value):
            self[key] = value

    class web_server_ini(Exception):
        pass

    with open(filename, 'r') as file:
        x = file.readlines()
    settings = []
    for line in x:
        if line.startswith('#'):
            pass
        else:
            settings.append(line.rstrip())
    dictionary = settings_dict()
    for setting in settings:
        try:
            name, value = setting.split(': ')
            dictionary.join(name, value.strip("'"))
        except ValueError as ve:
            print(f'ValueError: {ve}\n"{setting}" is missing a value, adding in ""')
            if setting == 'url1' or setting == 'url2':
                print('\nNPlease fill out both urls in the web_server.ini file!')
                raise web_server_ini(f'No URL settings found!\nCheck: "{setting}"')
            else:    
                dictionary.join(setting.strip(': '), '')
    return dictionary['url1'], dictionary['url2']

def get_time(url1, url2):
    urls = (url1, url2)
    try:
        response = urequests.get(urls[0])      
        print("Status code:", response.status_code)
        print("Date:", response.headers['Date'])
        
        return response.headers['Date']
        
    except KeyboardInterrupt as e:
        print("Error:", e)
        try:
            response = urequests.get(urls[1])
            print("Status code:", response.status_code)
            print("Date:", response.headers['Date'])
            return response.headers['Date']
        except Exception as ee:
            print(f'Error: {ee}')
    except:
        print('Error has occured. RTC has been not updated. Failed to get new time.')

def update_rtc(time_str):
    if time_str == None:
        print('Error. Time string is invalid. Check the response from server.')
        sys.exit()
    months = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
    }
    weekdays = {
        'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6,
        'Sun': 7
    }
    
    # Split the string into components
    parts = time_str.split()
    weekday = weekdays[parts[0].strip(',')]
    day = int(parts[1])
    month = months[parts[2]]
    year = int(parts[3])
    time_parts = parts[4].split(':')
    hour = int(time_parts[0])
    minute = int(time_parts[1])
    second = int(time_parts[2])

    print(f'Weekday from website: {weekday}')

    
    # Convert the date to a tuple (year, month, day, hour, minute, second)
    p_time = time.mktime((year, month, day, hour, minute, second, 0, 0)) # type: ignore
    weekday = time.gmtime(p_time)[6]
    rtc = machine.RTC()
    print((year, month, day, hour, weekday, minute, second, 0))
    rtc.datetime((year, month, day, weekday, hour, minute, second, 0))
    print('RTC Updated.')
    # Return the parsed components as a tuple
    return year, month, day, hour, minute, second

def main():
    try:
        urls = (load_ini_file('web_server.ini'))
        print('Updating RTC.\n')
        rtc = machine.RTC()
        print(f'Current time stored in the RTC: {rtc.datetime()}')
        time_now = get_time(urls[0], urls[1])
        print(f'New time is: {update_rtc(time_now)}\n')
    except ValueError as ve:
        print(f'Error has occured. RTC has not been updated. -- Error {ve}')

# Code
main()
