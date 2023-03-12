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

class DIR:

    def __manual(self):
        print("*** File info")
        print("### USAGE:")
        print(" python rmdir.py <Directory ID>")

    def process(self):

        if len(sys.argv) == 2 and (sys.argv[1].lower() == 'help' or sys.argv[1].lower() == '-h'):
            self.__manual()

        elif len(sys.argv) == 2:
            directory_id = int(sys.argv[1])

            km = Container.KeyManager()
            ns = Container.NodeService()
        
            try:
                if ns.joined(km.getCurrentNodeName()):
                    if int(directory_id) == 0:
                        print("Can not delete root directory")
                        exit()

                    if len(km.getFiles(directory_id)) > 0:
                        dir = km.getDirectory(directory_id)
                        print("Directory {} has one or more files".format(dir['name']))
                        exit()

                    if len(km.getDirectories(directory_id)) > 0:
                        dir = km.getDirectory(directory_id)
                        print("Directory {} has one or more directories".format(dir['name']))
                        exit()

                    km.rmdir(directory_id)

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

upd = DIR()
upd.process()