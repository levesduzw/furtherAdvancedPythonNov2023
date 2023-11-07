from threading import Thread, Semaphore
from datetime import datetime
import requests
import csv

class WeatherGetter(Thread):
    URL_TEMPLATE = 'http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&APPID={api_key}'
    API_KEY = '957d663a2296945e39a56609740a2548'
    
    semaphore = None    # optional
    
    def __init__(self, city, output_file_rlock, threads=1):
        Thread.__init__(self)
        self.city = city
        self.output_file_rlock = output_file_rlock
        self.semaphore = Semaphore(threads)
        
    def query_website(self, query_url) -> list:
        """Queries website

        Returns:
            list of objects: (timestamp, city, temp, wind_speed, wind_dir)
        """        
        self.semaphore.acquire()
        response = requests.get(query_url)
        self.semaphore.release()
        data = response.json()
        self.temperature = data['main']['temp']  # access the temperature property from the JSON
        
        dt = datetime.fromtimestamp(data['dt'])
        
        
        return [datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                dt,
                self.city,
                data['main']['temp'],
                data['wind']['speed'],
                data['wind']['deg'],
                ]        

    def serialize(self, city_data):
        # timestamp	city	temp	wind_speed	wind_dir
        #city_dt = city_data[0].strftime('%Y-%m-%dT%H:%M:%SZ')
        city_dt = city_data[1].strftime('%Y-%m-%d %H:%M:%S')
        city_name = city_data[2]
        print(f'{city_dt} Writing {city_name} data to file...')
        with self.output_file_rlock:
            with open('weather_data.csv', 'a') as csvfile:
                csv_writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(city_data)
    
        
    def run(self):
        print(f'(Timestamp) Starting thread for city "{self.city}"')
        query_url = self.URL_TEMPLATE.format(city_name=self.city, api_key=self.API_KEY)
        
        city_data = self.query_website(query_url)
        self.serialize(city_data)
        
        print(f'(Timestamp) Got temperature {self.temperature} for city "{self.city}"')
        
        return None
    