class CipherNotExist(Exception):
    def __init__(self, cipher):
        self.cipher = cipher