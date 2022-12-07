from NessKeys.exceptions.CrcCheck import CrcCheck
from NessKeys.interfaces.Cryptor import Cryptor
from Crypto.Hash import SHA256

class PasswordCryptor:
    def __init__(self, cryptor: Cryptor, Password: str):
        self.cryptor = cryptor
        sha256 = SHA256.new(data=bytes(Password, 'utf8'))
        sha256.block_size = self.cryptor.getBlockSize()
        self.key = sha256.digest()

    def encrypt(self, data: bytes) -> bytes:
        return self.cryptor.encrypt(data, self.key)

    def decrypt(self, data: bytes, crc_check: bytes) -> bytes:
        decrypted = self.cryptor.decrypt(data, self.key)
        crc = self.crc(decrypted)

        if crc != crc_check:
            raise CrcCheck()

        return decrypted

    def crc(self, data: bytes) -> bytes:
        sha256 = SHA256.new(data=data)
        return sha256.digest()