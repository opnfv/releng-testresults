from tornado.web import asynchronous
from tornado.gen import coroutine
from tornado.escape import json_encode

from api.handlers import BaseHandler
from api.service.scenario import ScenarioTableResult


class Result(BaseHandler):
    @asynchronous
    @coroutine
    def get(self):
        self._set_header()

        scenario = self.get_argument('scenario', None)
        version = self.get_argument('version', 'master')
        installer = self.get_argument('installer', None)
        iteration = int(self.get_argument('iteration', 10))

        yield self._get_scenario_data(scenario, version, installer, iteration)

    @coroutine
    def _get_scenario_data(self, scenario, version, installer, iteration):
        results = ScenarioTableResult(scenario, version, installer, iteration)
        result = yield results.get()
        self.write(json_encode(result))
        self.finish()
