class DeployResultCreateRequest():
    def __init__(
        self, build_id='', scenario='', stop_date='', start_date='',
        upstream_job_name='', version='', pod_name='', criteria='',
        installer='', upstream_build_id='', job_name='', details=''):
        self.build_id = build_id
        self.scenario = scenario
        self.stop_date = stop_date
        self.start_date = start_date
        self.upstream_job_name = upstream_job_name
        self.version = version
        self.pod_name = pod_name
        self.criteria = criteria
        self.installer = installer
        self.upstream_build_id = upstream_build_id
        self.job_name = job_name
        self.details = details
