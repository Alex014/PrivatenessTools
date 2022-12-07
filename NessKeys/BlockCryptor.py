import NessKeys.interfaces.Cryptor as Cryptor
import os, math

class BlockCryptor:
    def __init__(self, cryptor: Cryptor, block_size = 1048576):
        self.block_size = block_size
        self.cryptor = Cryptor

    def encrypt(filename_in: str, filename_out: str):
        filesize = os.path.getsize(filename_in)
        blocks = math.ceil(filesize / self.block_size)

        f_in = open(filename_in, "r")
        f_out = open(filename_out, "w")

        for i in range(blocks):
            block = f_in.read(self.block_size)
            encrypted_block = self.cryptor.encrypt(block)
            f_out.write(encrypted_block)

        f_in.close()
        f_out.close()


    def decrypt(filename_in: str, filename_out: str):
        filesize = os.path.getsize(filename_in)
        blocks = math.ceil(filesize / self.block_size)

        f_in = open(filename_in, "r")
        f_out = open(filename_out, "w")

        for i in range(blocks):
            block = f_in.read(self.block_size)
            encrypted_block = self.cryptor.decrypt(block)
            f_out.write(encrypted_block)

        f_in.close()
        f_out.close()