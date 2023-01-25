from NessKeys.interfaces.NessKey import NessKey
from NessKeys.exceptions.LeafBuildException import LeafBuildException

class UserLocal(NessKey):

    def __init__(self, keydata: dict):
        
        if not("filedata" in keydata):
            raise LeafBuildException("No filedata parameter", "/filedata")
            
        filedata = keydata["filedata"]

        if not ("vendor" in filedata and "type" in filedata and "for" in filedata):
            raise LeafBuildException("No vendor|type|for in filedata parameter", "/filedata/*")

        if not (filedata["vendor"] == "Privateness" and filedata["type"] == "key" and filedata["for"] == "user-local"):
            raise LeafBuildException("Wrong filetype", "/filedata/*")

        if not ("keys" in keydata and "username" in keydata and "nonce" in keydata):
            raise LeafBuildException("Not all parameters in place", "/*")

        keys = keydata["keys"]

        if not ("private" in keys and "public" in keys and "verify" in keys):
            raise LeafBuildException("Not all keys in place", "/keys/*")

        self.__username = keydata["username"]
        self.__nonce = keydata["nonce"]
        self.__private_key = keydata["keys"]["private"]
        self.__public_key = keydata["keys"]["public"]
        self.__verify_key = keydata["keys"]["verify"]

    def compile(self) -> dict:
        userdata = {
            "filedata": {
                "vendor": "Privateness",
                "type": "key",
                "for": "user-local"
            },
            "username": self.__username,
            "nonce": self.__nonce,
            "keys": {
                "private": self.__private_key,
                "public": self.__public_key,
                "verify": self.__verify_key
            },
        }

        return userdata

    def worm(self) -> str:
        return ""
        
    def nvs(self) -> str:
        return ""
        
    def print(self):
        return "Privateness Local User Key <{}>".format(self.__username)

    def filename():
        return "userlocal.key.json"

    def getFilename(self):
        return "userlocal.key.json"

    def getUsername(self):
        return self.__username

    def getNonce(self):
        return self.__nonce

    def getPrivateKey(self):
        return self.__private_key

    def getPublicKey(self):
        return self.__public_key

    def getVerifyKey(self):
        return self.__verify_key