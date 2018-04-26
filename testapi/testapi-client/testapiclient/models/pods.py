class PodCreateRequest(object):
    def __init__(self, name='', mode='', details='', role=''):
        self.name = name
        self.mode = mode
        self.details = details
        self.role = role
