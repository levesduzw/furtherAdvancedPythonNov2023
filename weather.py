import time
from WeatherGetter import WeatherGetter


def main():
    wg = WeatherGetter()
    wg.get_weather()

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    total = end-start
    print(f'Total time {total:.8f} seconds')