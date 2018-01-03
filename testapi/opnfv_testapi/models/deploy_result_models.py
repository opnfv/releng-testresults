from opnfv_testapi.models import base_models
from opnfv_testapi.tornado_swagger import swagger


@swagger.model()
class DeployResultCreateRequest(base_models.ModelBase):
    def __init__(self,
                 installer=None,
                 version=None,
                 pod_name=None,
                 job_name=None,
                 build_id=None,
                 scenario=None,
                 upstream_job_name=None,
                 upstream_build_id=None,
                 criteria=None,
                 start_date=None,
                 stop_date=None,
                 details=None):
        self.installer = installer
        self.version = version
        self.pod_name = pod_name
        self.job_name = job_name
        self.build_id = build_id
        self.scenario = scenario
        self.upstream_job_name = upstream_job_name
        self.upstream_build_id = upstream_build_id
        self.criteria = criteria
        self.start_date = start_date
        self.stop_date = stop_date
        self.details = details


@swagger.model()
class DeployResult(base_models.ModelBase):
    def __init__(self,
                 _id=None,
                 installer=None,
                 version=None,
                 pod_name=None,
                 job_name=None,
                 build_id=None,
                 scenario=None,
                 upstream_job_name=None,
                 upstream_build_id=None,
                 criteria=None,
                 start_date=None,
                 stop_date="true",
                 details=None):
        self._id = _id
        self.installer = installer
        self.version = version
        self.pod_name = pod_name
        self.job_name = job_name
        self.build_id = build_id
        self.scenario = scenario
        self.upstream_job_name = upstream_job_name
        self.upstream_build_id = upstream_build_id
        self.criteria = criteria
        self.start_date = start_date
        self.stop_date = stop_date
        self.details = details

    def __eq__(self, other):
        res = all(getattr(self, k) == getattr(other, k)
                  for k in self.format().keys() if k != '_id')
        return res


@swagger.model()
class DeployResults(base_models.ModelBase):
    """
        @property deployresults:
        @ptype deployresults: C{list} of L{DeployResult}
    """
    def __init__(self):
        self.results = list()

    @staticmethod
    def attr_parser():
        return {'deployresults': DeployResult}
