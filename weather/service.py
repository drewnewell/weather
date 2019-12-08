import json
import urllib

from .client import Client


class Service:
    '''Base class for Weather services.'''

    def __init__(self, *args, **kwargs):
        self.client = Client()

    def fetch(self):
        raise NotImplementedError()


class OpenWeather(Service):
    '''Service to acess resources at openweathermap.org.'''

    def __init__(self, api_key, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.api_key = api_key

    def parse_response(self, response):
        '''Parse urllib response.'''
        body = response.readlines()
        try:
            return json.loads(body[0].decode())
        except json.decoder.JSONDecodeError:
            #TODO: more handling here for other types of reponses like xml
            raise Exception('invalid response format, try json.')

    def prepare_params(self, params):
        '''urlencode params and credentials for request.'''
        params['APPID'] = self.api_key
        return urllib.parse.urlencode(params)

    def fetch(self, url, *args, **kwargs):
        '''Base fetch method for all OpenWeather endpoints.'''
        base_url = 'https://api.openweathermap.org/data/2.5/'
        url = base_url + url + '?' + self.prepare_params(kwargs)
        return self.parse_response(self.client.fetch_result(url))
        
    def get_current(self, *args, **kwargs):
        '''Call current weather data for one location. (https://openweathermap.org/current)'''
        endpoint = 'weather'
        return self.fetch(endpoint, **kwargs)

    def get_forecast(self, *args, **kwargs):
        '''Call 5 day / 3 hour forecast data. (https://openweathermap.org/forecast5)'''
        endpoint = 'forecast'
        return self.fetch(endpoint, **kwargs)


class OtherWeather(Service):
    '''Another weather service API.'''
    
    def get_other_data(self, *args, **kwargs):
        '''Another endpoint with other data.'''
        pass
