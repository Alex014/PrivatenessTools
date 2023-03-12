from NessKeys.interfaces.Cryptor import Cryptor
from Crypto.Cipher import Salsa20 as salsa20

class Salsa20(Cryptor):

    def encrypt(self, data: bytes, key: bytes) -> bytes:
        cipher = salsa20.new(key=key)
        self.block_size = 32
        return cipher.nonce + cipher.encrypt(data)

    def decrypt(self, data: bytes, key: bytes) -> bytes:
        msg_nonce = data[:8]
        ciphertext = data[8:]
        cipher = salsa20.new(key=key, nonce=msg_nonce)
        return cipher.decrypt(ciphertext)

    def getCipher(self) -> str:
        return 'salsa20'

    def getBlockSize(self) -> int:
        return 32

    def getBlockAddition(self) -> int:
        return 8