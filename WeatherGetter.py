from threading import Thread

class WeatherGetter(Thread):
    def __init__(self):
        Thread.__init__(self)
        
    def get_weather(self):
        print(f'(Timestamp) Got weather for city xxx')