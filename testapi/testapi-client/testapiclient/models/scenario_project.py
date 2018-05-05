class ScenarioProjectCreateRequest:
    def __init__(self, project='', scores=[], trust_indicators=[], customs=[]):
        self.project = project
        self.scores = scores
        self.trust_indicators = trust_indicators
        self.customs = customs
