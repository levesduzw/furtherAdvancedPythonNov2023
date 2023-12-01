import requests
from microservices.my_proxy import get_swapi_data

def get_person_info():
    return get_swapi_data(category='person', id='1', silent=False)