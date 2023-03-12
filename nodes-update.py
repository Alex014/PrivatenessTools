import os
import sys
import glob
from pathlib import Path
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
from NessKeys.cryptors.Salsa20 import Salsa20

from NessKeys.exceptions.BlockchainSettingsFileNotExist import BlockchainSettingsFileNotExist
from NessKeys.exceptions.NodesFileDoesNotExist import NodesFileDoesNotExist
from NessKeys.exceptions.EmptyNodesList import EmptyNodesList
from NessKeys.exceptions.NodeError import NodeError
from NessKeys.exceptions.NodeNotInList import NodeNotInList

from NessKeys.keys.BlockchainRPC import BlockchainRPC as BlockchainRpcKey
from NessKeys.keys.Nodes import Nodes
from NessKeys.keys.MyNodes import MyNodes

import getpass
import lxml.etree as etree
import requests

from ness.BlockchainRPC import BlockchainRPC

from framework.Container import Container

class NodesUpdater:

    def __manual(self):
        print("*** Remote nodes update UTILITY")
        print("### DESCRIPTION:")
        print("  Service node list update from blockchain or remote node")
        print("### USAGE:")
        print("#### Update from blockchain (if RPC connection settings olready exist)")
        print(" python nodes-update.py blockchain")
        print(" python nodes-update.py blk")
        print("#### Update from blockchain (connect to Emercoin RPC and save connection settings)")
        print(" python nodes-update.py blk rpc-host rpc-port rpc-user rpc-password")
        print("#### Update from remote node")
        print(" python nodes-update.py node <remote-node-url>")
        print("#### Update from remote node (random node fron existing nodes list)")
        print(" python nodes-update.py node")
        print("#### Auto update (try to update from random node, on error try to update from blockchain")
        print(" python nodes-update.py")

    def listNodesFromBlockchain(self, ip: str, port: int, user: str, password: str) -> dict:
        blk = BlockchainRPC(ip, port, user, password)
        nodes = {}
        records = blk.listNodes()

        for record in records['result']:
            name = record['name']

            record_full = blk.showResource(name)
            name = name.split(':')
            name = name[3:]
            name = ':'.join(name)
            worm_text = record_full['result']['value']

            try:
                # print(worm_text)
                worm = etree.XML(worm_text)
                node = worm.find("node")
                
                if node.attrib['type'].lower() == 'ness':
                    nd = {
                        'type': 'ness',
                        'url': node.attrib['url'],
                        'public': node.attrib['public'],
                        'verify': node.attrib['verify'],
                        'nonce': node.attrib['nonce'],
                        'tags': node.attrib['tags'].split(',')
                    }

                    if 'tariff' in node.attrib:
                        nd['tariff'] = float(node.attrib['tariff'])
                    else:
                        nd['tariff'] = 0

                    nodes[name] = nd
                    
                    print('+', end = " ", flush = True)
            except:
                pass

        print("")

        return nodes

    def listNodesFromRemoteNode(self, node_url: str) -> dict:
        print("### Updating nodes list from remote node {}".format(node_url))

        ns = Container.NodeService()
        result = ns.nodesList(node_url)

        if result['result'] == 'data':
            print("+ {}".format(len(result['data'])))
            return result['data']
        elif result['result'] == 'error':
            raise NodeError(result['error'])

        raise NodeError("Unknown error")

    def updateNodesFromBlockchain(self):
        km = Container.KeyManager()

        print("### Updating nodes list from blockchain")

        blk = km.getBlockchainSettings()
        nodes = self.listNodesFromBlockchain(blk['host'], blk['port'], blk['user'], blk['password'])
        # print(nodes)
        km.saveNodesList(nodes)

        return True

    def updateNodesFromRemoteNode(self):
        km = Container.KeyManager()

        node = km.getRandomNode()
        # print(node)
        nodes = self.listNodesFromRemoteNode(node['url'])
        # print(nodes)
        km.saveNodesList(nodes)

        return True

    def updateNodes(self):
            try:
                self.updateNodesFromRemoteNode()
                return True
            except EmptyNodesList as e:
                print ("* Failed to list nodes from remote node")
            except NodeError as e:
                print ("* Node error '{}'".format(e.error))
            except NodesFileDoesNotExist as e:
                print("NODES LIST file not found.")
                print("RUN python nodes-update.py node node-url")
                print("OR")
                print("RUN python nodes-update.py blk rpc-host rpc-port rpc-user rpc-password")
            except Exception as e:
                print ("* Error '{}'".format(str(e)))


            try:
                self.updateNodesFromBlockchain()
            except BlockchainSettingsFileNotExist as e:
                print("Blockchain settings not found.")
                print("RUN python nodes-update.py blk rpc-host rpc-port rpc-user rpc-password")
            except Exception as e:
                print ("* Error '{}'".format(str(e)))

    def process(self):
        km = Container.KeyManager()

        if len(sys.argv) == 6 and (sys.argv[1].lower() == 'blk' or sys.argv[1].lower() == 'blockchain'):
            host = sys.argv[2]
            port = int(sys.argv[3])
            user = sys.argv[4]
            password = sys.argv[5]

            nodes = self.listNodesFromBlockchain(host, port, user, password)

            km.saveNodesList(nodes)

            km.saveBlockchainSettings(host, port, user, password)

        elif len(sys.argv) == 2 and (sys.argv[1].lower() == 'blk' or sys.argv[1].lower() == 'blockchain'):
            try:
                self.updateNodesFromBlockchain()
            except BlockchainSettingsFileNotExist as e:
                print("Blockchain settings not found.")
                print("RUN python nodes-update.py blk rpc-host rpc-port rpc-user rpc-password")
            except Exception as e:
                print ("* Error '{}'".format(str(e)))

        elif len(sys.argv) == 3 and sys.argv[1].lower() == 'node':
            node_name = sys.argv[2]

            try:
                nodes = self.listNodesFromRemoteNode(node_name)
                # print(nodes)
                km.saveNodesList(nodes)
            except NodeError as e:
                print ("* Node error '{}'".format(e.error))
            except Exception as e:
                print ("* Error '{}'".format(str(e)))

        elif len(sys.argv) == 2 and sys.argv[1].lower() == 'node':
            try:
                self.updateNodesFromRemoteNode()
            except NodesFileDoesNotExist as e:
                print("NODES LIST file not found.")
                print("RUN python nodes-update.py node node-url")
            except EmptyNodesList as e:
                print ("* Empty nodes list in nodes.json file")
            except NodeError as e:
                print ("* Node error '{}'".format(e.error))
            except Exception as e:
                print ("* Error '{}'".format(str(e)))

        elif len(sys.argv) == 2 and (sys.argv[1].lower() == 'help' or sys.argv[1].lower() == '-h'):
            self.__manual()

        else:
            self.updateNodes()

upd = NodesUpdater()
upd.process()