import abc
from collections import defaultdict

import six
from tornado.gen import coroutine
from tornado.gen import Return

from api.service.result import ResultCache

PROJECTS = ['fastdatastacks', 'barometer', 'sfc', 'sdnvpn', 'doctor', 'parser']


def _set(key, llist):
    return set(x[key] for x in llist)


def _filter(key, value, llist):
    return filter(lambda x: x[key] == value, llist)


class ScenarioTableResult(object):

    def __init__(self, scenario, version, installer, iteration):
        self.scenario = scenario
        self.version = version
        self.installer = installer
        self.iteration = iteration

    @coroutine
    def get(self):
        results = yield ResultCache.get(self.version)
        results = self._filter_result(results)
        results = self._struct_result(results)

        raise Return(results)

    def _filter_result(self, results):
        results = [x for x in results if x['build_tag']]
        if self.installer:
            results = _filter('installer', self.installer, results)
        if self.scenario:
            results = _filter('scenario', self.scenario, results)
        return results

    def _struct_result(self, results):

        return {
            s: self._struct_scenario(_filter('scenario', s, results))
            for s in _set('scenario', results)
        }

    def _struct_scenario(self, data):
        return sorted([
            HandlerFacade.get_result(b, _filter('build_tag', b, data))
            for b in _set('build_tag', data)
        ], key=lambda x: x['date'], reverse=True)[:self.iteration]


class HandlerFacade(object):

    @classmethod
    def get_result(cls, index, data):
        if not data:
            return {}

        cls._change_name_to_functest(data)
        data = cls._sort_by_start_date(data)

        return {
            'id': index,
            'date': data[0]['start_date'],
            'version': data[0]['version'],
            'installer': data[0]['installer'],
            'projects': cls._get_projects_data(data)
        }

    @classmethod
    def _sort_by_start_date(cls, data):
        return sorted(data, key=lambda x: x['start_date'])

    @classmethod
    def _get_projects_data(cls, data):

        return {
            p: HANDLER_MAP[p](_filter('project_name', p, data)).struct()
            for p in _set('project_name', data)
        }

    @classmethod
    def _change_name_to_functest(cls, data):
        for ele in data:
            if ele['project_name'] in PROJECTS:
                ele['project_name'] = 'functest'


@six.add_metaclass(abc.ABCMeta)
class ProjectHandler(object):

    def __init__(self, data):
        self.data = data

    def struct(self):
        return self._struct_project_data()

    def _struct_project_data(self):
        return {
            'gating': self._gating()
        }

    @abc.abstractmethod
    def _gating(self):
        pass


class DefaultHandler(ProjectHandler):

    def _struct_project_data(self):
        return {}

    def _gating(self):
        pass


class FunctestHandler(ProjectHandler):

    def _gating(self):
        if all([x['criteria'] == 'PASS' for x in self.data]):
            return 'PASS'
        else:
            return 'FAIL'


HANDLER_MAP = defaultdict(lambda: DefaultHandler, functest=FunctestHandler)
