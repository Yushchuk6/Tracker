import json

from model.simulator import Simulator

res = {
    'type': None,
    'data': None,
}


class SimulatorController:
    def __init__(self, model):
        self.model = model

    def get_path_json(self):
        data = {
            'latlon': self.model.get_path(),
        }

        res['type'] = 'path'
        res['data'] = data
        return json.dumps(res)

    def get_trackers_json(self):
        data = {
            'latlon': self.model.get_trackers(),
        }

        res['type'] = 'trackers'
        res['data'] = data
        return json.dumps(res)

    def get_target_json(self, time):
        data = {
            'latlon': self.model.get_target(time),
        }

        res['type'] = 'target'
        res['data'] = data
        return json.dumps(res)

    def get_target_guess_json(self, time):
        data = {
            'latlon': self.model.get_target_guess(time),
        }

        res['type'] = 'target_guess'
        res['data'] = data
        return json.dumps(res)
