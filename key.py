import os
import sys
import glob
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
from NessKeys.cryptors.Salsa20 import Salsa20

from NessKeys.exceptions.KeyIndexException import KeyIndexException
from NessKeys.exceptions.LeafBuildException import LeafBuildException
from NessKeys.exceptions.CrcCheck import CrcCheck

import getpass

class Key:

    def __manual(self):
        print("*** PrivateNess KEY UTILITY")
        print("### DESCRIPTION:")
        print("  Privateness keys infrastructure management")
        print("### USAGE:")
        print("### List Keys")
        print("#### Show all contents of keyfile")
        print("  list {dirpath]")
        print("### Show Key")
        print("#### Show all contents of keyfile")
        print(" show <keyfile>")
        print("#### show nvs name (for blockchain)")
        print(" nvs <keyfile>")
        print("#### Show <worm> for blockchain (if there are any)")
        print(" worm <keyfile>")
        print("#### Show all encrypted keys (if there are any)")
        print(" list <keyfile>")
        print("### Pack keyfiles into encrypted keyfile")
        print(" pack <keyfile1,keyfile2, ...> <encrypted keyfile>")
        print("### Unpack keyfiles from encrypted keyfile")
        print(" unpack <encrypted keyfile>")
        print("### Save local keyfiles into encrypted keyfile")
        print(" save <encrypted keyfile>")
        print("### Restore local keyfiles from encrypted keyfile")
        print(" restore <encrypted keyfile>")

    def __getKM(self):
        storage = StorageJson()
        maker = KeyMakerNess()
        return KeyManager(storage, maker)

    def process(self):
        if len(sys.argv) == 3 and sys.argv[1].lower() == 'show':
            filename = sys.argv[2]
            try:
                km = self.__getKM()
                print(km.showKey(filename))
            except json.decoder.JSONDecodeError as e:
                print("File format error")
            except LeafBuildException as e:
                print("File format error: \"{}\" path: {}".format(e.msg, e.path))

        elif len(sys.argv) == 3 and sys.argv[1].lower() == 'nvs':
            filename = sys.argv[2]
            try:
                km = self.__getKM()
                print(km.showKeyNVS(filename))
            except json.decoder.JSONDecodeError as e:
                print("File format error")
            except LeafBuildException as e:
                print("File format error: \"{}\" path: {}".format(e.msg, e.path))

        elif len(sys.argv) == 3 and sys.argv[1].lower() == 'worm':
            filename = sys.argv[2]
            try:
                km = self.__getKM()
                print(km.showKeyWorm(filename))
            except json.decoder.JSONDecodeError as e:
                print("File format error")
            except LeafBuildException as e:
                print("File format error: \"{}\" path: {}".format(e.msg, e.path))

        elif len(sys.argv) == 2 and sys.argv[1].lower() == 'list':
            km = self.__getKM()
            files = glob.glob('*.key.json')
            
            for filename in files:
                print(" *** {}".format(filename))
                try:
                    print(km.showKey(filename))
                except json.decoder.JSONDecodeError as e:
                    print("File format error")
                except LeafBuildException as e:
                    print("File format error: \"{}\" path: {}".format(e.msg, e.path))

        elif len(sys.argv) == 3 and sys.argv[1].lower() == 'list':
            file_arg = sys.argv[2]

            if os.path.exists(file_arg): 
                if os.path.isfile(file_arg):
                    # Packed file listing
                    km = self.__getKM()

                    password = getpass.getpass("Type password:")

                    try:
                        km.listKeys(file_arg, password)
                    except LeafBuildException as e:
                        print("File format error: \"{}\" path: {}".format(e.msg, e.path))
                    except CrcCheck as e:
                        print("Wrong password (CRC check error)")
                else:
                    # Directory listing

                    km = self.__getKM()
                    path = file_arg + '/*.key.json'
                    files = glob.glob(path)
                    
                    for filename in files:
                        print(" *** {}".format(filename))
                        try:
                            print(km.showKey(filename))
                        except json.decoder.JSONDecodeError as e:
                            print("File format error")
                        except LeafBuildException as e:
                            print("File format error: \"{}\" path: {}".format(e.msg, e.path))

        elif len(sys.argv) == 4 and sys.argv[1].lower() == 'pack':
            km = self.__getKM()
            packet_keyfile = sys.argv[3]
            keys = sys.argv[2]

            password = getpass.getpass("Type password:")
            password2 = getpass.getpass("Confirm password:")

            if password != password2:
                print("Passwords does not match")
                return False

            try:
                km.packKeys(keys.split(','), packet_keyfile, password)
            except LeafBuildException as e:
                print("File format error: \"{}\" path: {}".format(e.msg, e.path))

        elif len(sys.argv) == 3 and sys.argv[1].lower() == 'unpack':
            km = self.__getKM()

            password = getpass.getpass("Type password:")

            try:
                km.unpackKeys(sys.argv[2], password)
            except LeafBuildException as e:
                print("File format error: \"{}\" path: {}".format(e.msg, e.path))
            except CrcCheck as e:
                print("Wrong password (CRC check error)")

        elif len(sys.argv) == 3 and sys.argv[1].lower() == 'save':
            print(" * Not implemented yet * ")
        elif len(sys.argv) == 3 and sys.argv[1].lower() == 'restore':
            print(" * Not implemented yet * ")
        else:
            self.__manual()

kkk = Key()
kkk.process()