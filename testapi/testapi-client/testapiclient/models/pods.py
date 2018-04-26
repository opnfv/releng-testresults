import json
import ast


class Pod(object):
    def __init__(self, **kwarg):
        for key in kwarg:
            self.__dict__[key] = kwarg[key]

    @classmethod
    def from_json(cls, json_str):
        json_dict = ast.literal_eval(json.dumps(json_str))
        return cls(**json_dict)
