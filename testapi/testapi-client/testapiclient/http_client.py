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
        print r.json() if r.status_code < 300 else r.text
        return r

    def _request(self, method, *args, **kwargs):
        return getattr(user.User.session, method)(*args, **kwargs)

    def post(self, url, data):
        return self._parse_response('Create',
                                    self._request('post', url,
                                                  data=json.dumps(data),
                                                  headers=self.headers))

    def put(self, url, data):
        return self._parse_response('Update',
                                    self._request('put', url,
                                                  data=json.dumps(data),
                                                  headers=self.headers))

    def delete(self, url, *args):
        data = json.dumps(args[0]) if len(args) > 0 else None
        return self._parse_response('Delete',
                                    self._request('delete', url,
                                                  data=data,
                                                  headers=self.headers))

    def _parse_response(self, request, response):
        print ' '.join([request,
                        'success' if response.status_code < 300
                        else 'failed: {}'.format(response.text)])
        return response


def http_request(method, *args, **kwargs):
    client = HTTPClient.get_Instance()
    return getattr(client, method)(*args, **kwargs)


def get(url):
    return http_request('get', url)


def post(url, data):
    return http_request('post', url, data)


def put(url, data):
    return http_request('put', url, data)


def delete(url, data=None):
    return http_request('delete', url, data)
