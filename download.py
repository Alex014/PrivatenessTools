import os
import sys

from framework.Container import Container

from NessKeys.exceptions.MyNodesFileDoesNotExist import MyNodesFileDoesNotExist
from NessKeys.exceptions.NodesFileDoesNotExist import NodesFileDoesNotExist
from NessKeys.exceptions.NodeNotFound import NodeNotFound
from NessKeys.exceptions.NodeError import NodeError
from NessKeys.exceptions.AuthError import AuthError

import requests

class Noder:

    def __manual(self):
        print("*** File download")
        print("### USAGE:")
        print("#### Download file from service node")
        print(" python download.py <file_shadowname> [path]")

    def process(self):

        if len(sys.argv) == 2 and (sys.argv[1].lower() == 'help' or sys.argv[1].lower() == '-h'):
            self.__manual()

        elif len(sys.argv) == 2:
            shadowname = sys.argv[1]

            km = Container.KeyManager()
            ns = Container.NodeService()
            fs = Container.FilesService()
            
            try:
                if ns.joined(km.getCurrentNodeName()):
                    km.initFilesAndDirectories()

                    km.setFileStatus(shadowname, 'w')
                    fs.download(shadowname)
                    km.setFileStatus(shadowname, 'd')
                    fs.decrypt(shadowname)
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

        elif len(sys.argv) == 3:
            shadowname = sys.argv[1]
            path = sys.argv[2]

            km = Container.KeyManager()
            ns = Container.NodeService()
            fs = Container.FilesService()
            
            try:
                if ns.joined(km.getCurrentNodeName()):
                    km.initFilesAndDirectories()

                    km.setFileStatus(shadowname, 'w')
                    fs.download(shadowname, path)
                    km.setFileStatus(shadowname, 'd')
                    fs.decrypt(shadowname, path)
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

upd = Noder()
upd.process()