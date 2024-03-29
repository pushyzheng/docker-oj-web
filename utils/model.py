# encoding:utf-8
import json
import copy


class JsonSerializableMixin(object):

    def to_json_string(self):
        return json.dumps(self, default=lambda obj: obj.__dict__)

    def from_json_string(self, json_string):
        data = json.loads(json_string)

        for key in self.__dict__.keys():
            if key in data:
                setattr(self, key, data[key])

    def __str__(self):
        return str(self.__dict__)


class ModelParent(object):
    def to_dict(self):
        res = copy.copy(self.__dict__)
        res.pop('_sa_instance_state')

        return res

    def from_dict(self, data):
        for key in data.keys():
            setattr(self, key, data[key])

    def __str__(self):
        return str(self.__dict__)
