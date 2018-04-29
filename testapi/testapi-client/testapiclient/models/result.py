from testapiclient.models import base_modal as base


class ResultRequest(base.BaseModel):
    def __init__(
        self, project_name='', scenario='', case_name='', pod_name='',
        installer='', version='', stop_date='', build_tag='', criteria='',
        start_date='', details=''):
        self.project_name = project_name
        self.scenario = scenario
        self.case_name = case_name
        self.pod_name = pod_name
        self.installer = installer
        self.version = version
        self.stop_date = stop_date
        self.build_tag = build_tag
        self.criteria = criteria
        self.start_date = start_date
        self.details = details


class Result(ResultRequest):
    def __init__(
        self, _id='', project_name='', scenario='', case_name='', pod_name='',
        installer='', version='', stop_date='', build_tag='', criteria='',
        start_date='', details=''):
        self.project_name = project_name
        self.scenario = scenario
        self.case_name = case_name
        self.pod_name = pod_name
        self.installer = installer
        self.version = version
        self.stop_date = stop_date
        self.build_tag = build_tag
        self.criteria = criteria
        self.start_date = start_date
        self.details = details
        self._id = _id
        super(Result, self).__init__(
            project_name, scenario, case_name, pod_name,
            installer, version, build_tag, criteria,
            start_date, details)
