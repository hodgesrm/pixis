from .parse import ext_regex
from .parse import get_object


class Paths:
    def __init__(self, dikt):
        self.dikt = {}
        self.extensions = []
        for key, value in dikt.items():
            if ext_regex.match(key):
                self.extensions.append({key: value})
            else:
                self.dikt[key] = get_object('/', value)
