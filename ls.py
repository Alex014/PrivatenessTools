import os
import sys

from framework.Container import Container

from NessKeys.exceptions.MyNodesFileDoesNotExist import MyNodesFileDoesNotExist
from NessKeys.exceptions.NodesFileDoesNotExist import NodesFileDoesNotExist
from NessKeys.exceptions.NodeNotFound import NodeNotFound
from NessKeys.exceptions.NodeError import NodeError
from NessKeys.exceptions.AuthError import AuthError

import requests

class Lister:

    def __manual(self):
        print("*** Current directory listing")
        print("### USAGE:")
        print("#### List files (current directory)")
        print(" python ls.py")
        print("#### RAW list files (as they are stored on service node)")
        print(" python ls.py raw")

    def process(self):

        if len(sys.argv) == 1:
            km = Container.KeyManager()
            ns = Container.NodeService()
            
            try:
                if ns.joined(km.getCurrentNodeName()):
                    km.initFilesAndDirectories()
                    fs = Container.FilesService()

                    fs.ls()
                else:
                    print("Current node is not set or not joined")

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

        elif len(sys.argv) == 2 and sys.argv[1].lower() == 'raw':
            km = Container.KeyManager()
            ns = Container.NodeService()
            
            try:
                if ns.joined(km.getCurrentNodeName()):
                    km.initFilesAndDirectories()
                    fs = Container.FilesService()

                    fs.raw()
                else:
                    print("Current node is not set or not joined")

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

ls = Lister()
ls.process()