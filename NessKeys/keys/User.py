from NessKeys.interfaces.NessKey import NessKey
from NessKeys.exceptions.LeafBuildException import LeafBuildException
from NessKeys.exceptions.KeyIndexException import KeyIndexException
import urllib.parse

class User(NessKey):

    def __init__(self, keydata: dict):

        if not("filedata" in keydata):
            raise LeafBuildException("No filedata parameter", "/filedata")
            
        filedata = keydata["filedata"]

        if not ("vendor" in filedata and "type" in filedata and "for" in filedata):
            raise LeafBuildException("No vendor|type|for in filedata parameter", "/filedata/*")

        if not (filedata["vendor"] == "Privateness" and filedata["type"] == "key" and filedata["for"] == "user"):
            raise LeafBuildException("Wrong filetype", "/filedata/*")

        if not ("username" in keydata and "nonce" in keydata and "tags" in keydata and "keys" in keydata):
            raise LeafBuildException("Not all parameters in place", "/*")

        keys = keydata["keys"]

        if not ("private" in keys and "public" in keys and "verify" in keys and "current" in keys):
            raise LeafBuildException("Not all keys in place", "/keys/*")

        if not (isinstance(keys["private"], list) and isinstance(keys["public"], list) and isinstance(keys["verify"], list)):
            raise LeafBuildException("Error in keys type", "/keys/*")

        if not (len(keys["private"]) == len(keys["public"]) == len(keys["verify"])):
            raise LeafBuildException("Wrong keys list length", "/keys/*")

        if not(isinstance(keys["current"], int) and len(keys["private"]) > int(keys['current'])):
            raise LeafBuildException("Wrong current key index", "/keys/*")

        self.__username = keydata["username"]
        self.__private_keys = keydata["keys"]["private"]
        self.__public_keys = keydata["keys"]["public"]
        self.__verify_keys = keydata["keys"]["verify"]
        self.__current_key = keydata["keys"]["current"]
        self.__nonce = keydata["nonce"]
        self.__tags = keydata["tags"].split(',')


    def compile(self) -> dict:
        userdata = {
            "filedata": {
                "vendor": "Privateness",
                "type": "key",
                "for": "user"
            },
            "username": self.__username,
            "keys": {
                "private": self.__private_keys,
                "public": self.__public_keys,
                "verify": self.__verify_keys,
                "current": self.__current_key
            },
            "nonce": self.__nonce,
            "tags": ",".join(self.__tags)
        }

        userdata["worm"] = self.__wrm(userdata)

        return userdata

    def worm(self) -> str:
        userdata = {
            "filedata": {
                "vendor": "Privateness",
                "type": "key",
                "for": "user"
            },
            "username": self.__username,
            "keys": {
                "private": self.__private_keys,
                "public": self.__public_keys,
                "verify": self.__verify_keys,
                "current": self.__current_key
            },
            "nonce": self.__nonce,
            "tags": ",".join(self.__tags)
        }

        return self.__wrm(userdata)
        
    def nvs(self) -> str:
        return "worm:user:ness:" + self.__username
        
    def print(self):
        return "Privateness User Key <{}>".format(self.__username) \
            + "\nKeys count: {}".format(len(self.__private_keys)) \
            + "\nCurrent key: {}".format(self.__current_key)

    def getFilename(self):
        return urllib.parse.quote_plus(self.__username) + ".key.json"

    def __wrm(self, user: dict):
        linesep = '\n'
        tab = '\t'
        tab2 = '\t\t'
        tab3 = '\t\t\t'

        current = user["keys"]["current"]

        keys = linesep

        for i in range(0, len(user["keys"]["public"]) - 1):
            if current == i:
                cc = " current=\"current\" "
            else:
                cc = ''

            keys += tab3 + "<key public=\"" + user["keys"]["public"][i] + "\"  verify=\"" + user["keys"]["verify"][i] \
                + "\"" + cc + "/>" + linesep

        worm = "<worm>" + linesep + \
            tab + "<user type=\"ness\" nonce=\"" + user["nonce"] + "\" tags=\"" \
               + user["tags"] + "\">" + linesep + \
            tab2 + "<keys>" + keys + \
            tab2 + "</keys>" + linesep + \
            tab2 + "<!-- Here tags may be different for each type of user -->" + linesep + \
            tab + "</user>" + linesep + \
            "</worm>"

        return worm

    def getUsername(self):
        return self.__username

    def getTags(self):
        return self.__tags

    def getNonce(self):
        return self.__nonce

    def getPrivateKeys(self):
        return self.__private_keys

    def getPublicKeys(self):
        return self.__public_keys

    def getVerifyKeys(self):
        return self.__verify_keys

    def getPrivateKey(self):
        return self.__private_keys[self.__current_key]

    def getPublicKey(self):
        return self.__public_keys[self.__current_key]

    def getVerifyKey(self):
        return self.__verify_keys[self.__current_key]

    def changeKeypair(self, new_index: int):
        if new_index > (len(self.__private_keys) - 1) or new_index < 0:
            raise KeyIndexException(new_index, (len(self.__private_keys) - 1) )

        self.__current_key = new_index