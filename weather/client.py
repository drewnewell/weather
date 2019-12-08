import urllib.request


class Client:
    '''Basic request and response handler.'''

    def fetch_result(self, url, *args, **kwargs):
        '''Fetch a request or prepared url.'''
        return urllib.request.urlopen(url)
