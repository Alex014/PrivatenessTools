import os
import sys

from framework.Container import Container
from services.ServicesManager import ServicesManager

from NessKeys.exceptions.MyNodesFileDoesNotExist import MyNodesFileDoesNotExist
from NessKeys.exceptions.NodesFileDoesNotExist import NodesFileDoesNotExist
from NessKeys.exceptions.NodeNotFound import NodeNotFound
from NessKeys.exceptions.NodeError import NodeError
from NessKeys.exceptions.AuthError import AuthError

import requests

class Noder:

    def __manual(self):
        print("*** File info")
        print("### USAGE:")
        print(" python fileinfo.py <file_id>")

    def process(self):

        if len(sys.argv) == 2 and (sys.argv[1].lower() == 'help' or sys.argv[1].lower() == '-h'):
            self.__manual()

        elif len(sys.argv) == 2:
            file_id = sys.argv[1]

            km = Container.KeyManager()
            sm = ServicesManager(km.getUserLocalKey())
            
            try:
                node_name = km.getCurrentNodeName()

                if sm.joined(km.getNodesKey(), node_name):
                    fileinfo = sm.fileinfo(km.getNodesKey(), km.getMyNodesKey(), node_name, file_id)

                    print(" *** fileinfo *** ")
                    print(fileinfo)

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