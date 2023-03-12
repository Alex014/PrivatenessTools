import os
import sys

from framework.Container import Container

from NessKeys.exceptions.MyNodesFileDoesNotExist import MyNodesFileDoesNotExist
from NessKeys.exceptions.NodesFileDoesNotExist import NodesFileDoesNotExist
from NessKeys.exceptions.NodeNotFound import NodeNotFound
from NessKeys.exceptions.NodeError import NodeError
from NessKeys.exceptions.AuthError import AuthError

import requests
from prettytable import PrettyTable

class Noder:

    def __manual(self):
        print("*** Remove file")
        print("### USAGE:")
        print(" python remove.py <file_shadowname>")
        print("##### Remove local copy of file:")
        print(" python remove.py local <file_shadowname>")

    def process(self):

        if len(sys.argv) == 2 and (sys.argv[1].lower() == 'help' or sys.argv[1].lower() == '-h'):
            self.__manual()

        elif len(sys.argv) == 2:
            file_shadowname = sys.argv[1]

            km = Container.KeyManager()
            ns = Container.NodeService()
            fs = Container.FilesService()
        
            try:
                if ns.joined(km.getCurrentNodeName()):
                    fs.remove(file_shadowname)
                    km.removeFile(file_shadowname)

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

        elif len(sys.argv) == 3 and sys.argv[1].lower() == 'local':
            file_shadowname = sys.argv[2]

            km = Container.KeyManager()
            ns = Container.NodeService()
            fs = Container.FilesService()
        
            try:
                if ns.joined(km.getCurrentNodeName()):
                    if km.getFile(file_shadowname) == False:
                        print("Shadowname {} not found".format(file_shadowname))
                        exit()
                    
                    fs.removeLocal(file_shadowname)
                    km.clearFilePath(file_shadowname)

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