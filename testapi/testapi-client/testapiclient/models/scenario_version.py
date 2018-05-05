class ScenarioVersionCreateRequest:
    def __init__(self, version='', owner='', projects=[]):
        self.version = version
        self.owner = owner
        self.projects = projects
