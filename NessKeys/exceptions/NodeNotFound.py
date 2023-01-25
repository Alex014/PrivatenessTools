class NodeNotFound(Exception):
    def __init__(self, node: str):
        self.node = node