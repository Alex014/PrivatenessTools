import os
import sys

from framework.Container import Container

from NessKeys.exceptions.MyNodesFileDoesNotExist import MyNodesFileDoesNotExist
from NessKeys.exceptions.NodesFileDoesNotExist import NodesFileDoesNotExist
from NessKeys.exceptions.NodeNotFound import NodeNotFound
from NessKeys.exceptions.NodeError import NodeError
from NessKeys.exceptions.AuthError import AuthError
from NessKeys.exceptions.FileNotExist import FileNotExist

import requests
from prettytable import PrettyTable

class DIR:

    def __manual(self):
        print("*** Move to other directory")
        print("### USAGE:")
        print(" python move.py <File shadowname or Directory ID> <Directory ID>")

    def process(self):

        if len(sys.argv) == 2 and (sys.argv[1].lower() == 'help' or sys.argv[1].lower() == '-h'):
            self.__manual()

        elif len(sys.argv) == 3:
            km = Container.KeyManager()
            ns = Container.NodeService()

            try:
                ID = sys.argv[1]
                parent_id = int(sys.argv[2])
                dir = km.getDirectory(parent_id)

                if dir == False:
                    print("Directory {} not found".format(parent_id))
                    exit(0)

                if ns.joined(km.getCurrentNodeName()):
                    if km.isFile(ID):
                        km.moveFile(ID, parent_id)
                    else:
                        km.moveDir(int(ID), parent_id)

                    print(' *** Moved to ' + dir['name'])

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
            except FileNotExist as e:
                print("File {} does not exist".format(e.filename))

        else:
            self.__manual()

upd = DIR()
upd.process()