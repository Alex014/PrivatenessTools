from NessKeys.interfaces.NessKey import NessKey
from NessKeys.exceptions.LeafBuildException import LeafBuildException

class Encrypted(NessKey):

    def __init__(self, keydata: dict):
        if not("filedata" in keydata):
            raise LeafBuildException("No filedata parameter", "/filedata")
            
        filedata = keydata["filedata"]

        if not ("vendor" in filedata and "type" in filedata and "cipher" in filedata):
            raise LeafBuildException("No vendor|type|for in filedata parameter", "/filedata/*")
            
        self.__for = filedata["for"]

        if not (filedata["vendor"] == "Privateness" and filedata["type"] == "encrypted-keys"):
            raise LeafBuildException("Wrong filetype", "/filedata/*")

        if not("cipher" in filedata):
            raise LeafBuildException("No cipher parameter", "/cipher")

        if not("keys" in keydata):
            raise LeafBuildException("No keys parameter", "/keys")

        if not("crc" in keydata):
            raise LeafBuildException("No crc parameter", "/crc")

        self.__cipher = filedata["cipher"]
        self.__keys = keydata["keys"]
        self.__crc = keydata["crc"]

        if not(type(self.__keys) == list):
            raise LeafBuildException("Wrong keys type", "/keys")

        if not(type(self.__crc) == list):
            raise LeafBuildException("Wrong crc type", "/crc")

    def compile(self) -> dict:
        appdata = {
            "filedata": {
                "vendor": "Privateness",
                "type": "encrypted-keys",
                "for": self.__for,
                "cipher": self.__cipher
            },
            "keys": self.__keys,
            "crc": self.__crc
        }
        
        return appdata

    def worm(self) -> str:
        return ""
        
    def nvs(self) -> str:
        return ""
        
    def print(self):
        return "Privateness Encrypted Key Storage for {}\nKeys count: {}\nCipher: {}".format(self.__for, len(self.__keys), self.__cipher)

    def getFilename(self):
        return "encrypted.keys.json"

    def getKeys(self):
        return self.__keys

    def setKeys(self, keys: list):
        self.__keys = keys

    def getCrc(self):
        return self.__crc

    def setCrc(self, crc: list):
        self.__crc = crc

    def addKey(self, key: str):
        self.__keys.append(key)

    def getCipher(self):
        return self.__cipher