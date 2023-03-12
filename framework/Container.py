from NessKeys.KeyManager import KeyManager
from NessKeys.StorageJson import StorageJson
from NessKeys.KeyMakerNess import KeyMakerNess

from services.node import node
from services.files import files

from NessKeys.interfaces.output import output as ioutput

from NessKeys.ConsoleOutput import ConsoleOutput


class Container:
    def KeyManager() -> KeyManager:
        storage = StorageJson()
        maker = KeyMakerNess()
        return KeyManager(storage, maker)

    def NodeService() -> node:
        km = Container.KeyManager()
        return node(km.getUserLocalKey(), km.getNodesKey(), km.getMyNodesKey(), Container.output())

    def FilesService() -> files:
        km = Container.KeyManager()
        return files(km.getUserLocalKey(), km.getNodesKey(), km.getMyNodesKey(), km.getFilesKey(), km.getDirectoriesKey(), Container.output())

    def output() -> ioutput:
        return ConsoleOutput()
