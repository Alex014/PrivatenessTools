from NessKeys.interfaces.NessKey import NessKey
from NessKeys.exceptions.LeafBuildException import LeafBuildException
import urllib.parse

class Faucet(NessKey):

    def __init__(self, keydata: dict):

        if not("filedata" in keydata):
            raise LeafBuildException("No filedata parameter", "/filedata")
            
        filedata = keydata["filedata"]

        if not ("vendor" in filedata and "type" in filedata and "for" in filedata):
            raise LeafBuildException("No vendor|type|for in filedata parameter", "/filedata/*")

        if not (filedata["vendor"] == "Privateness" and filedata["type"] == "key" and filedata["for"] == "faucet"):
            raise LeafBuildException("Wrong filetype", "/filedata/*")

        if not ("keys" in keydata and "url" in keydata):
            raise LeafBuildException("Not all parameters in place", "/*")

        keys = keydata["keys"]

        if not ("private" in keys and "verify" in keys):
            raise LeafBuildException("Not all keys in place", "/keys/*")

        self.__private_key = keydata["keys"]["private"]
        self.__verify_key = keydata["keys"]["verify"]
        self.__url = keydata["url"]

    def compile(self) -> dict:
        nodedata = {
            "filedata": {
                "vendor": "Privateness",
                "type": "key",
                "for": "faucet"
            },
            "keys": {
                "private": self.__private_key,
                "verify": self.__verify_key
            },
            "url": self.__url
        }

        nodedata["worm"] = self.__wrm(nodedata)

        return nodedata

    def worm(self) -> str:
        nodedata = {
            "filedata": {
                "vendor": "Privateness",
                "type": "key",
                "for": "faucet"
            },
            "keys": {
                "private": self.__private_key,
                "verify": self.__verify_key
            },
            "url": self.__url
        }

        return self.__wrm(nodedata)
        
    def nvs(self) -> str:
        return "worm:faucet:ness:" + self.__url
        
    def print(self):
        return "Privateness Faucet Key: <{}>".format(self.__url)

    def getFilename(self):
        return urllib.parse.quote_plus(self.__url) + ".key.json"

    def __wrm(self, nodedata: dict):
        linesep = '\n'
        tab = '\t'
        tab2 = '\t\t'

        worm = "<worm>" + linesep + \
            tab + "<faucet type=\"ness\" url=\"" + nodedata["url"] + "\"></faucet>" + linesep + \
            "</worm>"

        return worm

    def getPrivateKey(self):
        return self.__private_key

    def getVerifyKey(self):
        return self.__verify_key

    def getUrl(self):
        return self.__url