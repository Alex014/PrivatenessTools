import os
import sys
from base64 import b64encode
from base64 import b64decode
import json
import urllib.parse
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from nacl.signing import SigningKey, VerifyKey
from nacl.public import PrivateKey, PublicKey
from nacl.encoding import Base64Encoder
import validators
import lxml.etree as etree

import uuid
import NessKeys.Prng as prng
from NessKeys.KeyManager import KeyManager
from NessKeys.StorageJson import StorageJson
from NessKeys.KeyMakerNess import KeyMakerNess

from NessKeys.exceptions.KeyIndexException import KeyIndexException

class Keygen:

    def __is_integer(self, n):
        try:
            int(n)
        except ValueError:
            return False
        else:
            return True

    def __manual(self):
        print("*** PrivateNess KEY GENERATOR")
        print("### DESCRIPTION:")
        print("  Generates ciphers for NESS service nodes and NESS service node clients")
        print("  Works on ed25519 for keypairs")
        print("  Adjustable entropy when generating private keys")
        print("### USAGE:")
        print("#### Generate user")
        print("  user <username> <Keypair count> \"coma,separated,tags\" <Entropy level>")
        print("  Example: $ python keygen.py user user1 10 \"Hello,World\" 5")
        print("#### Generate node")
        print("  node <Node URL> <Tariff> master-user-name \"coma,separated,tags\"  <Entropy level>")
        print("  Example: $ python keygen.py node http://my-node.net 111 master \"Hello,World\" 5")
        print("#### Change user's keypair")
        print("  change <User Key File> <new keypair index>")
        print("  Example: $ python keygen.py change user.key.json 2")
        print("#### Generate seed")
        print("  seed <length> <Entropy level>")
        print("  Example: $ python keygen.py seed 32 5")
        print("#### Show version")
        print("  $ python codegen.py version")
        print("  $ python codegen.py -v")
        print("#### Show this manual")
        print("  $ python codegen.py help")
        print("  $ python codegen.py -h")

    def process(self):
        if len(sys.argv) == 6 and sys.argv[1].lower() == 'user':
            username = sys.argv[2]

            if self.__is_integer(sys.argv[3]):
                keypair_count = int(sys.argv[3])
            else:
                print("<Keypair count> must be integer")
                return False

            tags = sys.argv[4]

            if self.__is_integer(sys.argv[5]):
                entropy = int(sys.argv[5])

                if entropy < 1:
                    entropy = 1
            else:
                print("<Entropy level> must be integer")
                return False

            storage = StorageJson()
            maker = KeyMakerNess()
            manager = KeyManager(storage, maker)

            return manager.createUserKey(username, keypair_count, tags, entropy)

        elif len(sys.argv) == 7 and sys.argv[1].lower() == 'node':
            url = sys.argv[2]

            if self.__is_integer(sys.argv[3]):
                tariff = int(sys.argv[3])
            else:
                print("<Tariff> must be integer")
                return False

            master_user = sys.argv[4]
            tags = sys.argv[5]

            if self.__is_integer(sys.argv[6]):
                entropy = int(sys.argv[6])

                if entropy < 1:
                    entropy = 1
            else:
                print("<Entropy level> must be integer")
                return False

            storage = StorageJson()
            maker = KeyMakerNess()
            manager = KeyManager(storage, maker)

            return manager.createNodeKey(url, tariff, master_user, tags, entropy)

        elif len(sys.argv) == 4 and sys.argv[1].lower() == 'change':
            key_filename = sys.argv[2]

            if self.__is_integer(sys.argv[3]):
                key_index = int(sys.argv[3])
            else:
                print("<new keypair index> must be integer")
                return False

            storage = StorageJson()
            maker = KeyMakerNess()
            manager = KeyManager(storage, maker)

            try:
                manager.changeUserKeypair(key_filename, key_index)
            except KeyIndexException as e:
                print("Index %i out of range (from 0 to %i)" % (e.index, e.max))
                return False

            return True

        elif len(sys.argv) == 4 and sys.argv[1].lower() == 'seed':

            if self.__is_integer(sys.argv[2]):
                length = int(sys.argv[2])

                if length < 16:
                    length = 16
            else:
                print("<length> must be integer")
                return False

            if self.__is_integer(sys.argv[3]):
                entropy = int(sys.argv[3])

                if entropy < 1:
                    entropy = 1
            else:
                print("<Entropy level> must be integer")
                return False
            
            generator = prng.UhePrng()

            for i in range (1, entropy):
                rand = ''
                with open('/dev/random', 'rb') as file:
                    rand = b64encode(file.read(1024)).decode('utf-8')
                    file.close()

                generator.add_entropy(rand, str(uuid.getnode()))

                print('+', end = " ", flush = True)

            print("")
            print (generator.string(length))

        else:
            self.__manual()

keygen = Keygen()
keygen.process()
