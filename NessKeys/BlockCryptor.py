import NessKeys.interfaces.Cryptor as Cryptor
from NessKeys.interfaces.output import output as ioutput
import os, math

class BlockCryptor:
    def __init__(self, cryptor: Cryptor, key: bytes, output: ioutput, block_size = 1048576):
        self.block_size = block_size
        self.cryptor = cryptor
        self.output = output
        self.key = key

    def encrypt(self, filename_in: str, filename_out: str):
        filesize = os.path.getsize(filename_in)
        rbc = self.block_size - self.cryptor.getBlockAddition()
        blocks = math.ceil(filesize / rbc)
        
        f_in = open(filename_in, "rb")
        f_out = open(filename_out, "wb")

        for i in range(blocks):
            block = f_in.read(rbc)
            encrypted_block = self.cryptor.encrypt(block, self.key)
            f_out.write(encrypted_block)
            self.output.out('+')

        f_in.close()
        f_out.close()


    def decrypt(self, filename_in: str, filename_out: str):
        filesize = os.path.getsize(filename_in)
        blocks = math.ceil(filesize / self.block_size)
        
        f_in = open(filename_in, "rb")
        f_out = open(filename_out, "wb")

        for i in range(blocks):
            block = f_in.read(self.block_size)
            decrypted_block = self.cryptor.decrypt(block, self.key)
            f_out.write(decrypted_block)
            self.output.out('+')

        f_in.close()
        f_out.close()