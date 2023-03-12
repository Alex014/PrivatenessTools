import os
import sys

from framework.Container import Container

from NessKeys.exceptions.NodesFileDoesNotExist import NodesFileDoesNotExist
from NessKeys.exceptions.NodeNotFound import NodeNotFound
from NessKeys.exceptions.NodeError import NodeError
from NessKeys.exceptions.AuthError import AuthError

import requests

class Noder:

    def __manual(self):
        print("*** Node manipulation")
        print("### USAGE:")
        print("#### List all nodes (previously fetched from blockchain or remote node):")
        print(" python node.py list")
        print("#### Set current node (you will be registered in that node):")
        print(" python node.py set <node-name>")

    def process(self):
        km = Container.KeyManager()

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
                node_name = sys.argv[2]

                if not km.isNodeInNodesList(node_name):
                    raise NodeNotFound(node_name)

                ns = Container.NodeService()

                shadowname = ns.joined(node_name)

                if shadowname == False:
                    shadowname = ns.join(node_name)
                    
                if not km.hasMyNodes():
                    km.initMyNodes(node_name, shadowname)
                else:
                    km.saveCurrentNode(node_name, shadowname)
                    km.changeCurrentNode(node_name)

            except NodesFileDoesNotExist as e:
                print("NODES LIST file not found.")
                print("RUN python nodes-update.py node node-url")
            except NodeNotFound as e:
                print("NODE '{}' is not in nodes list".format(e.node))
            except NodeError as e:
                print("Error on remote node ")
            except AuthError as e:
                print("Responce verification error")

        elif len(sys.argv) == 3 and sys.argv[1].lower() == 'info':
            node_url = sys.argv[2]
            ns = Container.NodeService()
            print( ns.nodeInfo(node_url) )

        elif len(sys.argv) == 2 and (sys.argv[1].lower() == 'help' or sys.argv[1].lower() == '-h'):
            self.__manual()

        else:
            self.__manual()

upd = Noder()
upd.process()