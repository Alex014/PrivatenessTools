from NessKeys.keys.MyNodes import MyNodes
from NessKeys.keys.Nodes import Nodes
from NessKeys.keys.UserLocal import UserLocal

from NessKeys.exceptions.NodeNotFound import NodeNotFound
from NessKeys.exceptions.NodeError import NodeError
from NessKeys.exceptions.AuthError import AuthError

import json
from ness.NessAuth import NessAuth
import requests

class ServicesManager:
    def __init__(self, localUserKey: UserLocal):

        self.localUserKey = localUserKey

        self.auth = NessAuth()

    def nodeInfo(node_url: str) -> dict:
        return json.loads(requests.get(node_url + '/node/info').text)

    def nodesList(node_url: str) -> dict:
        return json.loads(requests.get(node_url + '/node/nodes').text)

    def join(self, nodes: Nodes, node_name: str):
        currentNode = nodes.findNode(node_name)

        if currentNode == False:
            raise NodeNotFound(node_name)

        url = currentNode['url'] + "/node/join"

        result = self.auth.get_by_two_way_encryption(
            url, 
            '123', 
            currentNode['public'], 
            self.localUserKey.getPrivateKey(), 
            self.localUserKey.getUsername() )

        if result['result'] == 'error':
            raise NodeError()

        if not self.auth.verify_two_way_result(currentNode['verify'], result):
            raise AuthError()

        result = self.auth.decrypt_two_way_result(result, self.localUserKey.getPrivateKey())
        data = json.loads(result)
        
        return data['shadowname']

    def joined(self, nodes: Nodes, node_name: str):
        currentNode = nodes.findNode(node_name)

        if currentNode == False:
            raise NodeNotFound(node_name)

        url = currentNode['url'] + "/node/joined"

        result = self.auth.get_by_two_way_encryption(
            url, 
            '123', 
            currentNode['public'], 
            self.localUserKey.getPrivateKey(), 
            self.localUserKey.getUsername() )

        if result['result'] == 'error':
            raise NodeError()
        
        if not self.auth.verify_two_way_result(currentNode['verify'], result):
            raise AuthError()

        result = self.auth.decrypt_two_way_result(result, self.localUserKey.getPrivateKey())
        data = json.loads(result)

        if data['joined']:
            return data['shadowname']
        else:
            return False

    def userinfo(self, nodes: Nodes, myNodes: MyNodes):
        node_name = myNodes.getCurrentNode()
        myNode = myNodes.findNode(node_name)
        currentNode = nodes.findNode(node_name)

        if currentNode == False:
            raise NodeNotFound(node_name)

        shadowname = myNode['shadowname']

        url = currentNode['url'] + "/node/userinfo"
        result = self.auth.get_by_two_way_encryption(
            url, 
            '123', 
            currentNode['public'], 
            self.localUserKey.getPrivateKey(), 
            shadowname )

        if result['result'] == 'error':
            raise NodeError()

        if not self.auth.verify_two_way_result(currentNode['verify'], result):
            raise AuthError()

        result = self.auth.decrypt_two_way_result(result, self.localUserKey.getPrivateKey())
        data = json.loads(result)
        # print(data)

        return data['userinfo']