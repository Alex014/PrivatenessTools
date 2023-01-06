from NessKeys.interfaces.NessKey import NessKey
from NessKeys.exceptions.LeafBuildException import LeafBuildException

class BlockchainRPC(NessKey):

    def __init__(self, keydata: dict):
        
        if not("filedata" in keydata):
            raise LeafBuildException("No filedata parameter", "/filedata")
            
        filedata = keydata["filedata"]

        if not ("vendor" in filedata and "type" in filedata and "for" in filedata):
            raise LeafBuildException("No vendor|type|for in filedata parameter", "/filedata/*")

        if not (filedata["vendor"] == "Privateness" and filedata["type"] == "config" and filedata["for"] == "blockchain"):
            raise LeafBuildException("Wrong filetype", "/filedata/*")

        if not("rpc-host" in keydata):
            raise LeafBuildException("No rpc-host parameter", "/")

        if not("rpc-port" in keydata):
            raise LeafBuildException("No rpc-port parameter", "/")

        if not("rpc-user" in keydata):
            raise LeafBuildException("No rpc-user parameter", "/")

        if not("rpc-password" in keydata):
            raise LeafBuildException("No rpc-password parameter", "/")

        self.__host = keydata["rpc-host"]
        self.__port = keydata["rpc-port"]
        self.__user = keydata["rpc-user"]
        self.__password = keydata["rpc-password"]

    def compile(self) -> dict:
        appdata = {
            "filedata": {
                "vendor": "Privateness",
                "type": "config",
                "for": "blockchain"
            },
            "rpc-host": self.__host,
            "rpc-port": self.__port,
            "rpc-user": self.__user,
            "rpc-password": self.__password,
        }

        return appdata

    def worm(self) -> str:
        return ""
        
    def nvs(self) -> str:
        return ""

    def print(self):
        return "Privateness Blockchain Config"

    def filename():
        return "blockchain-rpc.json"

    def getFilename(self):
        return BlockchainRPC.filename()

    def getHost(self) -> str:
        return self.__host

    def getPort(self) -> str:
        return self.__port

    def getUser(self) -> str:
        return self.__user

    def getPassword(self) -> str:
        return self.__password
