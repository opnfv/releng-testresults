import json

import requests
from testapiclient import user


class HTTPClient(object):

    __instance = None
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    @staticmethod
    def get_Instance():
        """ Static access method. """
        if HTTPClient.__instance is None:
            HTTPClient()
        return HTTPClient.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if HTTPClient.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            HTTPClient.__instance = self

    def get(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        else:
            return r.text

    def session_request(self, method, *args, **kwargs):
        return getattr(user.User.session, method)(*args, **kwargs)

    def post(self, url, data):
        return self.session_request('post', url,
                                    data=json.dumps(data),
                                    headers=HTTPClient.headers)

    def put(self, url, data):
        return self.session_request('put', url,
                                    data=json.dumps(data),
                                    headers=HTTPClient.headers).text

    def delete(self, url, *args):
        if(args.__len__ > 0):
            r = self.session_request('delete', url,
                                     data=json.dumps(args[0]),
                                     headers=HTTPClient.headers)
        else:
            r = self.session_request('delete', url)
        return r.text


def http_request(method, *args, **kwargs):
    client = HTTPClient.get_Instance()
    return getattr(client, method)(*args, **kwargs)


def get(url):
    return http_request('get', url)


def post(url, data):
    return http_request('post', url, data)


def put(url, data):
    return http_request('put', url, data)


def delete(url, data):
    return http_request('delete', url, data)
