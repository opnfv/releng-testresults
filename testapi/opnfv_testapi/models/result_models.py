##############################################################################
# Copyright (c) 2015 Orange
# guyrodrigue.koffi@orange.com / koffirodrigue@gmail.com
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################
from opnfv_testapi.models import base_models
from opnfv_testapi.tornado_swagger import swagger


@swagger.model()
class ResultCreateRequest(base_models.ModelBase):
    def __init__(self,
                 pod_name=None,
                 project_name=None,
                 case_name=None,
                 installer=None,
                 version=None,
                 start_date=None,
                 stop_date=None,
                 details=None,
                 build_tag=None,
                 scenario=None,
                 criteria=None):
        self.pod_name = pod_name
        self.project_name = project_name
        self.case_name = case_name
        self.installer = installer
        self.version = version
        self.start_date = start_date
        self.stop_date = stop_date
        self.details = details
        self.build_tag = build_tag
        self.scenario = scenario
        self.criteria = criteria

    def __eq__(self, other):
        return all(getattr(self, k) == getattr(other, k)
                   for k in self.format().keys()
                   if k not in ['_id'])


@swagger.model()
class TestResult(ResultCreateRequest):
    def __init__(self, _id=None, **kwargs):
        super(TestResult, self).__init__(**kwargs)
        self._id = _id


@swagger.model()
class TestResults(base_models.ModelBase):
    """
        @property results:
        @ptype results: C{list} of L{TestResult}
    """
    def __init__(self):
        self.results = list()

    @staticmethod
    def attr_parser():
        return {'results': TestResult}
