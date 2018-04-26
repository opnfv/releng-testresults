import json
import ast


class PodCreateRequest(object):
    def __init__(self, name='', mode='', details='', role=""):
        self.name = name
        self.mode = mode
        self.details = details
        self.role = role


class Pod(PodCreateRequest):
    def __init__(self, **kwargs):
        self._id = kwargs.pop('_id', '')
        self.creation_date = kwargs.pop('creation_date', '')
        self.creator = kwargs.pop('creator', '')
        super(Pod, self).__init__(**kwargs)

    @classmethod
    def from_json(cls, json_str):
        json_dict = ast.literal_eval(json.dumps(json_str))
        return cls(**json_dict)
