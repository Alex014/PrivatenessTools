class KeyIndexException(Exception):
    def __init__(self, index, max):
        self.index = index
        self.max = max