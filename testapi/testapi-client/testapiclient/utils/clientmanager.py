import httplib
import json
import os
import urllib
import logging

import requests

LOG = logging.getLogger(__name__)


class ClientManager(object):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    def __init__(self, cli_options=None):
        self.cli_options = cli_options
        self.session = requests.Session()
        self._auth_completed = False

    @property
    def auth_required(self):
        return self._auth()

    def _auth(self):
        return {
            'name': self.cli_options.u,
            'pass': self.cli_options.p
        } if self.cli_options.u else None

    def auth(self):

        if self._auth_completed:
            return

        hostname = '{}{}{}'.format(os.environ.get('testapi_cas_auth_url'),
                                   urllib.quote(os.environ.get('testapi_url')),
                                   os.environ.get('testapi_cas_signin_return'))
        data = self._auth()
        data.update({'form_id': 'user_login'})
        LOG.debug('authenticating.....')
        response = self.session.post(hostname, data)
        if "login" in response.text:
            raise Exception('Authenticate failed')
        self._auth_completed = True

    def get(self, url):
        return self._parse_response('Get',
                                    self._request('get', url,
                                                  headers=self.headers))

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

    def _request(self, method, *args, **kwargs):
        return getattr(self.session, method)(*args, **kwargs)

    def _raise_failure(self, op, response):
        raise Exception('{} failed: {}'.format(op, response.reason))

    def _parse_response(self, op, response):
        if response.status_code == httplib.OK:
            return response.json() if op != 'Delete' else None
        else:
            self._raise_failure(op, response)
