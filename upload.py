import os
import sys
from base64 import b64encode
from base64 import b64decode
import uuid

from framework.Container import Container

from NessKeys.exceptions.MyNodesFileDoesNotExist import MyNodesFileDoesNotExist
from NessKeys.exceptions.NodesFileDoesNotExist import NodesFileDoesNotExist
from NessKeys.exceptions.NodeNotFound import NodeNotFound
from NessKeys.exceptions.NodeError import NodeError
from NessKeys.exceptions.AuthError import AuthError

import NessKeys.Prng as prng

import requests

class Uploader:

    def __manual(self):
        print("*** File upload")
        print("### USAGE:")
        print("#### Upload file on service node")
        print(" python upload.py <path to your file to upload>")

    def process(self):

        if len(sys.argv) == 2 and (sys.argv[1].lower() == 'help' or sys.argv[1].lower() == '-h'):
            self.__manual()

        elif len(sys.argv) == 2:
            filepath = sys.argv[1]

            if not os.path.exists(filepath):
                print("File '{}' does not exist".format(filepath))
                exit()

            km = Container.KeyManager()
            ns = Container.NodeService()
            
            try:
                if ns.joined(km.getCurrentNodeName()):
                    km.initFilesAndDirectories()
                    fs = Container.FilesService()

                    shadowname = km.addFile(filepath, '', '', 'u', km.getCurrentDir())
                    fs.upload(filepath, shadowname)
                    km.setFileStatus(shadowname, 'n')

            except MyNodesFileDoesNotExist as e:
                print("MY NODES file not found.")
                print("RUN python node.py set node-url")
            except NodesFileDoesNotExist as e:
                print("NODES LIST file not found.")
                print("RUN python nodes-update.py node node-url")
            except NodeNotFound as e:
                print("NODE '{}' is not in nodes list".format(e.node))
            except NodeError as e:
                print("Error on remote node: " + e.error)
            except AuthError as e:
                print("Responce verification error")


        elif len(sys.argv) == 3 and (sys.argv[1].lower() == 'enc' or sys.argv[1].lower() == 'encrypt'):
            filepath = sys.argv[2]

            if not os.path.exists(filepath):
                print("File '{}' does not exist".format(filepath))
                exit()

            km = Container.KeyManager()
            ns = Container.NodeService()
            
            try:
                if ns.joined(km.getCurrentNodeName()):
                    km.initFilesAndDirectories()

                    print(" *** Generating key ...")

                    generator = prng.UhePrng()

                    for i in range (1, 10):
                        rand = ''
                        with open('/dev/random', 'rb') as file:
                            rand = b64encode(file.read(1024)).decode('utf-8')
                            file.close()

                        generator.add_entropy(rand, str(uuid.getnode()))

                        print('+', end = " ", flush = True)

                    print("")
                    key = generator.string(32)
                    
                    shadowname = km.addFile(filepath, key, 'salsa20', 'e', km.getCurrentDir())

                    fs = Container.FilesService()

                    km.setFileStatus(shadowname, 'e')
                    encpath = fs.encrypt(filepath, shadowname)
                    km.setFileStatus(shadowname, 'u')
                    fs.upload(encpath, shadowname)
                    km.setFileStatus(shadowname, 'n')

            except MyNodesFileDoesNotExist as e:
                print("MY NODES file not found.")
                print("RUN python node.py set node-url")
            except NodesFileDoesNotExist as e:
                print("NODES LIST file not found.")
                print("RUN python nodes-update.py node node-url")
            except NodeNotFound as e:
                print("NODE '{}' is not in nodes list".format(e.node))
            except NodeError as e:
                print("Error on remote node: " + e.error)
            except AuthError as e:
                print("Responce verification error")

        else:
            self.__manual()

upd = Uploader()
upd.process()