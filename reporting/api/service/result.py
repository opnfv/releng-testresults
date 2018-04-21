import json
import logging
from collections import defaultdict

from tornado.gen import coroutine
from tornado.gen import Return
from tornado.httpclient import AsyncHTTPClient

from api import conf as consts
from api.extension.client import NoQueueTimeoutHTTPClient

LOG = logging.getLogger(__name__)
AsyncHTTPClient.configure(NoQueueTimeoutHTTPClient)


class Result(object):

    def __init__(self):
        self._url = '{}/results?period={}&version={}&page={}'
        self._client = AsyncHTTPClient()
        self._result = defaultdict(list)

    @property
    @coroutine
    def result(self):
        if not self._result:
            yield self.update_results()
        raise Return(self._result)

    @coroutine
    def update_results(self):
        LOG.info('start update results')

        for version in consts.versions:
            yield self._update_version_result(version)

        LOG.info('results update finished')

    @coroutine
    def _update_version_result(self, version):
        total_page = yield self._get_total_page(version)

        responses = yield self._fetch_results(version, total_page)

        self._update_version_dict(version, responses)

    @coroutine
    def _fetch_results(self, version, total_page):
        urls = [self._url.format(consts.base_url, consts.period, version, i)
                for i in range(1, total_page + 1)]
        responses = yield [self._client.fetch(url) for url in urls]
        raise Return(responses)

    @coroutine
    def _get_total_page(self, version):
        url = self._url.format(consts.base_url, consts.period, version, 1)
        response = yield self._client.fetch(url)
        raise Return(json.loads(response.body)['pagination']['total_pages'])

    def _update_version_dict(self, version, responses):
        for response in responses:
            results = json.loads(response.body)['results']
            for result in results:
                data = {k: v for k, v in result.items() if k != 'details'}
                self._result[version].append(data)


class ResultCache(Result):

    @classmethod
    @coroutine
    def update(cls):
        cls._check()

        yield cls.cache.update_results()

    @classmethod
    @coroutine
    def get(cls, version):
        cls._check()

        result = yield cls.cache.result
        raise Return(result[version])

    @classmethod
    def _check(cls):
        try:
            cls.cache
        except AttributeError:
            cls.cache = cls()
