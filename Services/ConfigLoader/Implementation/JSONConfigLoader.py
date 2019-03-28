from Services.ConfigLoader.API.ConfigLoader import ConfigLoader
from Services.Logger.Implementation.Logging import Logging
import json


class JSONConfigLoader(ConfigLoader):
    def __init__(self, path):
        self.path = path

    def parse(self):
        try:
            with open(self.path) as json_file:
                return json.load(json_file)
        except OSError:
            pass
