from NessKeys.interfaces.NessKey import NessKey
from NessKeys.interfaces.KeyMaker import KeyMaker

from NessKeys.keys.Node import Node as NodeKey
from NessKeys.keys.User import User as UserKey
from NessKeys.keys.UserLocal import UserLocal
from NessKeys.keys.Encrypted import Encrypted
from NessKeys.keys.BlockchainRPC import BlockchainRPC
from NessKeys.keys.Nodes import Nodes
from NessKeys.keys.MyNodes import MyNodes
from NessKeys.keys.Faucet import Faucet
from NessKeys.exceptions.LeafBuildException import LeafBuildException

class KeyMakerNess(KeyMaker):
    def make(self, keydata: dict) -> NessKey:
        if not("filedata" in keydata):
            raise LeafBuildException("No filedata parameter", "/filedata")

        filedata = keydata["filedata"]

        if not ("vendor" in filedata and "type" in filedata):
            raise LeafBuildException("No vendor|type in filedata parameter", "/filedata/*")

        vendor = filedata['vendor']
        _type = filedata['type']
        _for = filedata['for']

        if vendor == "Privateness" and _type == 'key' and _for == 'user':
            return UserKey(keydata)
        elif vendor == "Privateness" and _type == 'key' and _for == 'node':
            return NodeKey(keydata)
        elif vendor == "Privateness" and _type == 'key' and _for == 'user-local':
            return UserLocal(keydata)
        elif vendor == "Privateness" and _type == 'encrypted-keys':
            return Encrypted(keydata)
        elif vendor == "Privateness" and _type == 'config' and _for == 'blockchain':
            return BlockchainRPC(keydata)
        elif vendor == "Privateness" and _type == 'data' and _for == 'nodes-list':
            return Nodes(keydata)
        elif vendor == "Privateness" and _type == 'service' and _for == 'node':
            return MyNodes(keydata)
        elif vendor == "Privateness" and _type == 'key' and _for == 'faucet':
            return Faucet(keydata)

        return False