import os
import sys
import json

from NessKeys.keys.Nodes import Nodes
from NessKeys.keys.MyNodes import MyNodes

from NessKeys.StorageJson import StorageJson
from NessKeys.KeyMakerNess import KeyMakerNess
from NessKeys.KeyManager import KeyManager

from NessKeys.exceptions.NodesFileDoesNotExist import NodesFileDoesNotExist
from NessKeys.exceptions.EmptyNodesList import EmptyNodesList
from NessKeys.exceptions.NodeNotInList import NodeNotInList

import requests

class Noder:

    def __manual(self):
        print("*** Node manipulation")
        print("### USAGE:")
        print("#### List all nodes (previously fetched from blockchain or remote node):")
        print(" python node.py list")
        print("#### Set current node (node name usualy equals node url):")
        print(" python node.py set <node-name>")

    def __getKM(self):
        storage = StorageJson()
        maker = KeyMakerNess()
        return KeyManager(storage, maker)

    def process(self):
        km = self.__getKM()

        if len(sys.argv) == 2 and sys.argv[1].lower() == 'list':
            try:
                nodes = km.getNodesList()
                current_node = km.getCurrentNodeName()

                for node_name in nodes:
                    if current_node == node_name:
                        print ("### ==> " + node_name)
                    else:
                        print ("###     " + node_name)
                    print(nodes[node_name])
            except NodesFileDoesNotExist as e:
                print("NODES LIST file not found.")
                print("RUN python nodes-update.py node node-url")

        elif len(sys.argv) == 3 and sys.argv[1].lower() == 'set':
            try:
                km = self.__getKM()
                node_name = sys.argv[2]
                km.saveCurrentNode(node_name)
            except NodesFileDoesNotExist as e:
                print("NODES LIST file not found.")
                print("RUN python nodes-update.py node node-url")
            except NodeNotInList as e:
                print("NODE '{}' is not in nodes list".format(node_name))

        elif len(sys.argv) == 3 and sys.argv[1].lower() == 'info':
            node_url = sys.argv[2]
            print( json.loads(requests.get(node_url + '/node/info').text) )

        elif len(sys.argv) == 2 and (sys.argv[1].lower() == 'help' or sys.argv[1].lower() == '-h'):
            self.__manual()

        else:
            self.__manual()

upd = Noder()
upd.process()