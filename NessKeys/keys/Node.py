from NessKeys.interfaces.NessKey import NessKey
from NessKeys.exceptions.LeafBuildException import LeafBuildException
import urllib.parse

class Node(NessKey):

    def __init__(self, keydata: dict):

        if not("filedata" in keydata):
            raise LeafBuildException("No filedata parameter", "/filedata")
            
        filedata = keydata["filedata"]

        if not ("vendor" in filedata and "type" in filedata and "for" in filedata):
            raise LeafBuildException("No vendor|type|for in filedata parameter", "/filedata/*")

        if not (filedata["vendor"] == "Privateness" and filedata["type"] == "key" and filedata["for"] == "node"):
            raise LeafBuildException("Wrong filetype", "/filedata/*")

        if not ("keys" in keydata and "url" in keydata and "nonce" in keydata and "master-user" in keydata and "tags" in keydata and "tariff" in keydata):
            raise LeafBuildException("Not all parameters in place", "/*")

        keys = keydata["keys"]

        if not ("private" in keys and "public" in keys and "verify" in keys):
            raise LeafBuildException("Not all keys in place", "/keys/*")

        if not(isinstance(keydata["tariff"], int)):
            raise LeafBuildException("Wrong tariff type", "/tariff")

        self.__private_key = keydata["keys"]["private"]
        self.__public_key = keydata["keys"]["public"]
        self.__verify_key = keydata["keys"]["verify"]
        self.__url = keydata["url"]
        self.__nonce = keydata["nonce"]
        self.__master_user = keydata["master-user"]
        self.__tags = keydata["tags"].split(',')
        self.__tariff = keydata["tariff"]

    def compile(self) -> dict:
        nodedata = {
            "filedata": {
                "vendor": "Privateness",
                "type": "key",
                "for": "node"
            },
            "keys": {
                "private": self.__private_key,
                "public": self.__public_key,
                "verify": self.__verify_key
            },
            "url": self.__url,
            "nonce": self.__nonce,
            "master-user": self.__master_user,
            "tags": ",".join(self.__tags),
            "tariff": self.__tariff,
        }

        nodedata["worm"] = self.__wrm(nodedata)

        return nodedata

    def worm(self) -> str:
        nodedata = {
            "filedata": {
                "vendor": "Privateness",
                "type": "key",
                "for": "node"
            },
            "keys": {
                "private": self.__private_key,
                "public": self.__public_key,
                "verify": self.__verify_key
            },
            "url": self.__url,
            "nonce": self.__nonce,
            "master-user": self.__master_user,
            "tags": ",".join(self.__tags),
            "tariff": self.__tariff,
        }

        return self.__wrm(nodedata)
        
    def nvs(self) -> str:
        return "worm:node:ness:" + self.__url
        
    def print(self):
        return "Privateness Node Key: <{}>\nMaster User:<{}>\nTariff:<{}>".format(self.__url, self.__master_user, self.__tariff)

    def getFilename(self):
        return urllib.parse.quote_plus(self.__url) + ".key.json"

    def __wrm(self, nodedata: dict):
        linesep = '\n'
        tab = '\t'
        tab2 = '\t\t'

        worm = "<worm>"+linesep+\
            tab + "<node type=\"ness\" url=\"" + nodedata["url"] + "\" nonce=\"" + nodedata["nonce"] + "\"   " + \
            " verify=\"" + nodedata['keys']["verify"] + "\" public=\"" + nodedata['keys']["public"] + "\" master-user=\"" + \
            nodedata["master-user"] + "\" tariff=\"" + str(nodedata["tariff"]) + "\" tags=\"" + nodedata["tags"] + "\">" + linesep + \
            tab2 + "<!-- Here tags may be different for each type of node or each node -->" + linesep + \
            tab + "</node>" + linesep + \
            "</worm>"

        return worm

    def getTags(self):
        return self.__tags

    def getNonce(self):
        return self.__nonce

    def getPrivateKey(self):
        return self.__private_key

    def getPublicKey(self):
        return self.__public_key

    def getVerifyKey(self):
        return self.__verify_key

    def getUrl(self):
        return self.__url

    def getTariff(self):
        return self.__tariff

    def getMasterUser(self):
        return self.__master_user