from threading import Thread
import requests

class WeatherGetter(Thread):
    URL_TEMPLATE = 'http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&APPID={api_key}'
    API_KEY = '957d663a2296945e39a56609740a2548'
    
    
    def __init__(self, city):
        Thread.__init__(self)
        self.city = city
    
    def __call__(self):
        print(f'(Timestamp) Call weather for city "{self.city}"')
        
    def run(self):
        print(f'(Timestamp) Starting thread for city "{self.city}"')
        query_url = self.URL_TEMPLATE.format(city_name=self.city, api_key=self.API_KEY)
        print(f'query_url={query_url}')
        response = requests.get(query_url)
        data = response.json()
        self.temperature = data['main']['temp']  # access the temperature property from the JSON
        print(f'(Timestamp) Got temperature {self.temperature} for city "{self.city}"')