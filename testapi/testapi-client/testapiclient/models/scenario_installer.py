class ScenarioInstallerCreateRequest:
    def __init__(self, installer='', versions=[]):
        self.installer = installer
        self.versions = versions
