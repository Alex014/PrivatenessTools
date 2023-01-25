import os
import glob
import random
import sys
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

import NessKeys.interfaces.NessKey as NessKey
from NessKeys.keys.User import User as UserKey
from NessKeys.keys.Node import Node as NodeKey
from NessKeys.keys.UserLocal import UserLocal
from NessKeys.keys.Encrypted import Encrypted
from NessKeys.keys.BlockchainRPC import BlockchainRPC as BlockchainRpcKey
from NessKeys.keys.Nodes import Nodes
from NessKeys.keys.MyNodes import MyNodes
import NessKeys.interfaces.KeyMaker as KeyMaker
import NessKeys.interfaces.Storage as Storage
import NessKeys.interfaces.NessKey as NessKey
import NessKeys.interfaces.Cryptor as Cryptor
import uuid
import NessKeys.Prng as prng
from NessKeys.CryptorMaker import CryptorMaker
from NessKeys.PasswordCryptor import PasswordCryptor


from NessKeys.exceptions.BlockchainSettingsFileNotExist import BlockchainSettingsFileNotExist
from NessKeys.exceptions.NodesFileDoesNotExist import NodesFileDoesNotExist
from NessKeys.exceptions.EmptyNodesList import EmptyNodesList
from NessKeys.exceptions.NodeError import NodeError
from NessKeys.exceptions.NodeNotInList import NodeNotInList
from NessKeys.exceptions.UserLocalKeyFileDoesNotExist import UserLocalKeyFileDoesNotExist
class KeyManager:

    def __init__(self, storage: Storage, key_maker: KeyMaker):
        self.__storage = storage
        self.__key_maker = key_maker
        self.directory = str(Path.home()) + "/.privateness-keys"

    def fileName(self, filename: str) -> str:
        return self.directory + "/" + filename

    def fileExists(self, filename: str) -> bool:
        return os.path.exists(self.fileName(filename))

    def createUserKey(self, username: str, keypairs: int, tags: str, entropy: int):
        key_pairs = self.__keypairs(keypairs, entropy)
        filename = urllib.parse.quote_plus(username) + ".key.json"

        userdata = {
            "filedata": {
                "vendor": "Privateness",
                "type": "key",
                "for": "user"
            },
            "username": username,
            "keys": {
                'private': key_pairs['private'],
                'verify': key_pairs['verify'],
                'public': key_pairs['public'],
                'current': key_pairs['current']
            },
            "nonce": b64encode(get_random_bytes(16)).decode('utf-8'),
            "tags": tags
        }

        userkey = UserKey(userdata)
        self.__storage.save(userkey.compile(), filename)

    def createNodeKey(self, url: str, tariff: int, masterUser: str, tags: str, entropy: int):
        keypair = self.__keypair(entropy)
        filename = urllib.parse.quote_plus(url) + ".key.json"

        nodedata = {
            "filedata": {
                "vendor": "Privateness",
                "type": "key",
                "for": "node"
            },
            "keys": {
                "private": keypair[0],
                "verify": keypair[1],
                "public": keypair[2]
            },
            "url": url,
            "nonce": b64encode(get_random_bytes(16)).decode('utf-8'),
            "master-user": masterUser,
            "tags": tags,
            "tariff": tariff,
        }

        nodekey = NodeKey(nodedata)
        self.__storage.save(nodekey.compile(), filename)

    def __getKey(self, filename: str) -> NessKey:
        keydata = self.__storage.restore(filename)
        return self.__key_maker.make(keydata)

    def showKey(self, filename: str):
        Key = self.__getKey(filename)

        if Key:
            return Key.print()

    def showKeyFull(self, filename: str):
        Key = self.__getKey(filename)

        if Key:
            return Key.build()

    def showKeyNVS(self, filename: str):
        Key = self.__getKey(filename)

        if Key:
            return Key.nvs()

    def showKeyWorm(self, filename: str):
        Key = self.__getKey(filename)

        if Key:
            return Key.worm()

    def changeUserKeypair(self, filename: str, keypairIndex: int):
        userdata = self.__storage.restore(filename)
        userkey = UserKey(userdata)
        userkey.changeKeypair(keypairIndex)
        self.__storage.save(userkey.compile(), filename)

    def listKeys(self, filename: str, password: str = 'qwerty123'):
        cryptor = CryptorMaker.make('salsa20')
        pc = PasswordCryptor(cryptor, password)

        Key = self.__getKey(filename)
        packedKeys = Key.getKeys()
        crc = Key.getCrc()

        i = 0
        for packedKey in packedKeys:
            # Unpack key
            original_key = pc.decrypt( b64decode(packedKey), b64decode(crc[i]) ).decode('utf-8')
            # Restore key
            keydata = json.loads(original_key)
            key = self.__key_maker.make(keydata)
            # Print Key
            i += 1
            print(" # " + str(i))
            print(key.print())

        return True

    def unpackKeys(self, filename: str, password: str = 'qwerty123', dir = ""):
        cryptor = CryptorMaker.make('salsa20')
        pc = PasswordCryptor(cryptor, password)

        Key = self.__getKey(filename)
        packedKeys = Key.getKeys()
        crc = Key.getCrc()

        i = 0
        for packedKey in packedKeys:
            # Unpack key
            original_key = pc.decrypt( b64decode(packedKey), b64decode(crc[i]) ).decode('utf-8')
            # Restore key
            keydata = json.loads(original_key)
            key = self.__key_maker.make(keydata)
            # Save Key
            self.__storage.save(key.compile(), dir + key.getFilename())
            i += 1

        return True

    def packKeys(self, keysFiles: list, outFilename: str, password: str = 'qwerty123'):
        cryptor = CryptorMaker.make('salsa20')
        pc = PasswordCryptor(cryptor, password)
        keys = []
        crc = []

        for keysFile in keysFiles:
            # Load key
            Key = self.__getKey(keysFile)
            skey = Key.serialize()
            # CRC
            crc.append( b64encode(pc.crc(bytes(skey, 'utf8'))).decode('utf-8') )
            # Pack key
            skey = b64encode(pc.encrypt(bytes(skey, 'utf8'))).decode('utf-8')
            keys.append(skey)

        keydata = {
            "filedata": {
                "vendor": "Privateness",
                "type": "encrypted-keys",
                "for": "",
                "cipher": cryptor.getCipher()
            },
            "keys": keys,
            "crc": crc
        }

        encrypted = Encrypted(keydata)
        
        self.__storage.save(encrypted.compile(), outFilename)

    def hasUserLocal(self) -> bool:
        return self.fileExists(UserLocal.filename())

    def getUserLocalKey(self):
        filename = self.fileName(UserLocal.filename())

        if os.path.exists(filename):
            keydata = self.__storage.restore(filename)
            return UserLocal(keydata)
        else:
            raise UserLocalKeyFileDoesNotExist()


    def init(self, user_keyfile: str):
        userdata = self.__storage.restore(user_keyfile)
        userkey = UserKey(userdata)

        userdata = {
            "filedata": {
                "vendor": "Privateness",
                "type": "key",
                "for": "user-local"
            },
            "username": userkey.getUsername(),
            "nonce": userkey.getNonce(),
            "keys": {
                "private": userkey.getPrivateKey(),
                "public": userkey.getPublicKey(),
                "verify": userkey.getVerifyKey(),
            },
        }

        localkey = UserLocal(userdata)

        if not os.path.exists(self.directory):
            os.mkdir(self.directory)

        self.__storage.save(localkey.compile(), self.fileName(UserLocal.filename()))


    def init_node(self, node_keyfile: str):
        keydata = self.__storage.restore(node_keyfile)
        nodekey = NodeKey(keydata)

        node_data = {
            "master-user": nodekey.getMasterUser(),
            "nonce": nodekey.getNonce(),
            "private": nodekey.getPrivateKey(),
            "public": nodekey.getPublicKey(),
            "tariff": nodekey.getTariff(),
            "period": "7200",
            "delta": "1200",
            "url": nodekey.getUrl(),
            "verify": nodekey.getVerifyKey(),
            "slots": 10
        }

        self.__storage.save(node_data, 'node.json')

    def save(self, outFilename: str, password: str = 'qwerty123'):
        keysFiles = glob.glob(self.directory + "/*.json" )

        keysFilesWithDir = []
        for keyFile in keysFiles:
            keysFilesWithDir.append(keyFile)
        
        return self.packKeys(keysFilesWithDir, outFilename, password)

    def restore(self, inFilename: str, password: str = 'qwerty123'):
        return self.unpackKeys(inFilename, password, self.directory + '/')


    def hasBlockchainSettings(self) -> dict:
        return self.fileExists(BlockchainRPC.filename())


    def hasNodesList(self) -> bool:
        return self.fileExists(Nodes.filename())

    def getNodesKey(self):
        nodedata = self.__storage.restore(self.fileName(Nodes.filename()))
        return Nodes(nodedata)

    def getNodesList(self) -> list:
        nodedata = self.__storage.restore(self.fileName(Nodes.filename()))
        nodes = Nodes(nodedata)
        return nodes.compile()['nodes']

    def saveNodesList(self, modes: list):
        keydata = {
            "filedata": {
                "vendor": "Privateness",
                "type": "data",
                "for": "nodes-list"
            },
            "nodes": modes
        }

        nodes = Nodes(keydata)
        self.__storage.save(nodes.compile(), self.fileName(Nodes.filename()))

    def saveBlockchainSettings(self, host: str, port: int, user: str, password: str):
        keydata = {
            "filedata": {
                "vendor": "Privateness",
                "type": "config",
                "for": "blockchain"
            },
            "rpc-host": host,
            "rpc-port": port,
            "rpc-user": user,
            "rpc-password": password,
        }

        key = BlockchainRpcKey(keydata)

        self.__storage.save(key.compile(), self.fileName(BlockchainRpcKey.filename()))

    def getBlockchainSettings(self) -> dict:
        filename = self.fileName(BlockchainRpcKey.filename())

        if not os.path.exists(filename):
            raise BlockchainSettingsFileNotExist()

        keydata = self.__storage.restore(filename)
        key = BlockchainRpcKey(keydata)
        return {'host': key.getHost(), 'port': key.getPort(), 'user': key.getUser(), 'password': key.getPassword()}

    def listNodes(self) -> dict:
        filename = self.fileName(Nodes.filename())

        if not os.path.exists(filename):
            raise NodesFileDoesNotExist()

        keydata = self.__storage.restore(filename)
        key = Nodes(keydata)
        return key.getNodes()


    def getRandomNode(self) -> dict:
        nodes = self.listNodes()

        if (len(nodes) == 0):
            raise EmptyNodesList()

        rnd = random.randrange(0, len(nodes))
        cnt = 0
            
        for url in nodes:
            if cnt == rnd:
                return nodes[url]
            cnt += 1

    def hasMyNodes(self) -> bool:
        return os.path.exists( self.fileName(MyNodes.filename()) )

    def initMyNodes(self, node_name: str, user_shadowname: str):
        keydata = {
            "filedata": {
                "for": "node",
                "type": "service",
                "vendor": "Privateness"
            },
            "current-node": node_name,
            "my-nodes": {
                node_name: {
                    "shadowname": user_shadowname
                }
            }
        }

        key = MyNodes(keydata)

        self.__storage.save(key.compile(), self.fileName(MyNodes.filename()))

    def hasNodesList(self) -> bool:
        return os.path.exists( self.fileName(Nodes.filename()) )

    def getMyNodesKey(self):
        filename = self.fileName(MyNodes.filename())

        if not os.path.exists(filename):
            raise MyNodesFileDoesNotExist()

        keydata = self.__storage.restore(filename)

        return MyNodes(keydata)


    def isNodeInMyNodes(self, node_name: str) -> bool:
        key = self.getMyNodesKey()

        return (key.findNode(node_name) != False)

    def isNodeInNodesList(self, node_name: str) -> bool:
        filename = self.fileName(Nodes.filename())

        if not os.path.exists(filename):
            raise NodesFileDoesNotExist()

        keydata = self.__storage.restore(filename)
        key = Nodes(keydata)

        return (key.findNode(node_name) != False)

    def getCurrentNodeName(self) -> str:
        if self.hasMyNodes():
            key = self.getMyNodesKey()
            return key.getCurrentNode()
        else:
            return False

    def getCurrentNode(self) -> dict:
        nodes = self.listNodes()

        return nodes[self.getCurrentNodeName()]

    def saveCurrentNode(self, node_name: str, user_shadowname: str):
        key = self.getMyNodesKey()

        if not key.findNode(node_name):
            key.addNode(node_name, user_shadowname)
        else:
            key.updateNode(node_name, user_shadowname)

        self.__storage.save(key.compile(), self.fileName(MyNodes.filename()))


    def changeCurrentNode(self, node_name: str):
        key = self.getMyNodesKey()
        if not key.findNode(node_name):
            raise NodeNotInList()

        key.changeCurrentNode(node_name)

        self.__storage.save(key.compile(), self.fileName(MyNodes.filename()))

    def __zerofill(self, filename: str):
        sz = os.path.getsize(filename)
        strz = "".zfill(sz)
        
        f = open(filename, 'w')
        f.write(strz)
        f.close()

    def eraise(self, filename: str):
        self.__zerofill(filename)
        os.remove(filename)

    def eraiseAll(self):
        keysFiles = glob.glob(self.directory + "/*.json" )

        for keyFile in keysFiles:
            self.eraise(keyFile)

    def __keypair(self, entropy: int):

        return self.__keypair_seed(self.__generate_seed(entropy))

    def __keypairs(self, count: int, entropy: int):
        private_list = []
        verify_list = []
        public_list = []

        for i in range(0, count):
            keypair = self.__keypair_seed(self.__generate_seed(entropy))
            private_list.append(keypair[0])
            verify_list.append(keypair[1])
            public_list.append(keypair[2])

        return {'private': private_list, 'public': public_list, 'verify': verify_list, 'current': 0}

    def __keypair_seed(self, seed: bytes):
        SK = SigningKey(seed)
        signing_key = SK.generate()
        signing__key = signing_key.encode(encoder=Base64Encoder).decode('utf-8')
        private_key = PrivateKey(b64decode(signing__key))
        verify__key = signing_key.verify_key.encode(encoder=Base64Encoder).decode('utf-8')
        public__key = private_key.public_key.encode(encoder=Base64Encoder).decode('utf-8')

        return [signing__key, verify__key, public__key]

    def __generate_seed(self, entropy: int):
        generator = prng.UhePrng()

        for i in range (0, entropy):
            rand = ''
            with open('/dev/random', 'rb') as file:
                rand = b64encode(file.read(1024)).decode('utf-8')
                file.close()

            generator.add_entropy(rand, str(uuid.getnode()))

            print('+', end = " ", flush = True)

        print("")
        
        return generator.string(32).encode(encoding = 'utf-8')
