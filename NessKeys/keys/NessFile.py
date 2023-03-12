from NessKeys.interfaces.Leaf import Leaf
from NessKeys.exceptions.LeafBuildException import LeafBuildException

class NessFile(Leaf):

    def __init__(self, keydata: dict):

        if not("cipher" in keydata):
            raise LeafBuildException("No cipher parameter", "/cipher")

        if not("cipher-type" in keydata):
            raise LeafBuildException("No cipher-type parameter", "/cipher-type")

        if not("shadowname" in keydata):
            raise LeafBuildException("No shadowname parameter", "/shadowname")

        self.__cipher = keydata['cipher']
        self.__cipher_type = keydata['cipher-type']
        self.__shadowname = keydata['shadowname']
        self.__status = 'c'

    def compile(self) -> dict:
        filedata = {
            "cipher": self.__cipher,
            "cipher-type": self.__cipher_type,
            "shadowname": self.__shadowname,
            "status": self.__status,
        }

        return filedata

    def getCipher(self):
        return self.__cipher

    def getCipherType(self):
        return self.__cipher_type

    def getShadowname(self):
        return self.__shadowname

    def getStatus(self):
        return self.__status