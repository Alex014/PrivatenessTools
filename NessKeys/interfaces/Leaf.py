import json

class Leaf:
    def __init__(self, keydata: dict):
        pass

    def compile(self) -> dict:
        pass

    def serialize(self) -> str:
        return json.dumps(self.compile())