import NessKeys.interfaces.Cryptor as Cryptor
from NessKeys.cryptors.Salsa20 import Salsa20
from NessKeys.exceptions.CipherNotExist import CipherNotExist

class CryptorMaker:
    def make(cipher: str) -> Cryptor:
        if cipher == "salsa20":
            return Salsa20()
        else:
            raise CipherNotExist(cipher) 