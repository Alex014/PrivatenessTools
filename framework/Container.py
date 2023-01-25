from NessKeys.KeyManager import KeyManager
from NessKeys.StorageJson import StorageJson
from NessKeys.KeyMakerNess import KeyMakerNess

class Container:
    def KeyManager() -> KeyManager:
        storage = StorageJson()
        maker = KeyMakerNess()
        return KeyManager(storage, maker)
