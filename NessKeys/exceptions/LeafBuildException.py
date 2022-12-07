class LeafBuildException(Exception):
    def __init__(self, msg, path):
        self.path = path
        self.msg = msg