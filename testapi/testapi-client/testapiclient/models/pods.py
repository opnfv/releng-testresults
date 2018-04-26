import json
import ast


class PodCreateRequest(object):
    def __init__(self, name='', mode='', details='', role=''):
        self.name = name
        self.mode = mode
        self.details = details
        self.role = role


class Pod(PodCreateRequest):
    def __init__(
        self, _id='', creation_date='', creator='',
        name='', mode='', details='', role=''):
        self._id = _id
        self.creation_date = creation_date
        self.creator = creator
        super(Pod, self).__init__(name, mode, details, role)

    @classmethod
    def from_json(cls, json_str):
        json_dict = ast.literal_eval(json.dumps(json_str))
        return cls(**json_dict)
