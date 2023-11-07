import time
from threading import RLock
from WeatherGetter import WeatherGetter


def main():
    
    city_list = ('Sopron', 'Pécs', 'Budapest', 'Kecskemét', 'Debrecen')
    thread_list = []
    
    output_file_rlock = RLock()
    
    
    for city in city_list:
        thread = WeatherGetter(city, output_file_rlock, threads=1)
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