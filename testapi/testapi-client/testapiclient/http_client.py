import json

import requests


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

    def post(self, url, session, data):
        r = session.post(url,
                         data=json.dumps(data),
                         headers=HTTPClient.headers)
        return r

    def put(self, url, session, data):
        r = session.put(url,
                        data=json.dumps(data),
                        headers=HTTPClient.headers)
        return r.text

    def delete(self, url, session, *args):
        if(args.__len__ > 0):
            r = session.delete(url,
                               data=json.dumps(args[0]),
                               headers=HTTPClient.headers)
        else:
            r = session.delete(url)
        return r.text


def http_request(method, *args, **kwargs):
    client = HTTPClient.get_Instance()
    return getattr(client, method)(*args, **kwargs)


def get(url):
    return http_request('get', url)


def post(url, session, data):
    return http_request('post', url, session, data)


def put(url, session, data):
    return http_request('put', url, session, data)


def delete(url, session, data):
    return http_request('delete', url, session, data)
