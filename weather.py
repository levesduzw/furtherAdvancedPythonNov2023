import time
from threading import Thread
from WeatherGetter import WeatherGetter


def main():
    
    
    city_list = ('Sopron', 'Pécs', 'Budapest', 'Kecskemét', 'Debrecen')
    thread_list = []
    
    for city in city_list:
        #thread = Thread(target=wg, args=(city,))
        thread = WeatherGetter(city)
        thread_list.append(thread)
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    total = end-start
    print(f'Total time {total:.8f} seconds')    