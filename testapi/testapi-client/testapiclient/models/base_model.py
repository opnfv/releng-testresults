import json
import ast


class BaseModel():

    @classmethod
    def from_json(cls, json_str):
        json_dict = ast.literal_eval(json.dumps(json_str))
        return cls(**json_dict)
