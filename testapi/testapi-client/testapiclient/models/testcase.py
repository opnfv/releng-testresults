class TestCaseCreateRequest():
    def __init__(
        self, run='', name='', ci_loop='', tags='', url='',
        blocking='', domains='', dependencies='', version='',
        criteria='', tier='', trust='', catalog_description='',
        description=''):
        self.run = run
        self.name = name
        self.ci_loop = ci_loop
        self.tags = tags
        self.url = url
        self.blocking = blocking
        self.domains = domains
        self.dependencies = dependencies
        self.version = version
        self.criteria = criteria
        self.tier = tier
        self.trust = trust
        self.catalog_description = catalog_description
        self.description = description
