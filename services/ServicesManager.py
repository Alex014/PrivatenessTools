from NessKeys.keys.MyNodes import MyNodes
from NessKeys.keys.Nodes import Nodes
from NessKeys.keys.UserLocal import UserLocal

from NessKeys.exceptions.NodeNotFound import NodeNotFound
from NessKeys.exceptions.NodeError import NodeError
from NessKeys.exceptions.AuthError import AuthError

import json
from ness.NessAuth import NessAuth
import math
import os
import requests

class ServicesManager:
    def __init__(self, localUserKey: UserLocal):

        self.localUserKey = localUserKey

        self.auth = NessAuth()

        self.block_size = 1024**2

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
            raise NodeError(result['error'])
        
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

    def quota(self, username: str, node_url: str):
        myNode = myNodes.findNode(node_name)
        currentNode = nodes.findNode(node_name)    
        filename = os.path.basename(filepath)  
        
        if currentNode == False:
            raise NodeNotFound(node_name)

        shadowname = myNode['shadowname']

        url = currentNode['url'] + "/files/quota"

        joined = self.joined(username, node_url)

        if joined == False:
            return False

        result = self.auth.get_by_two_way_encryption(url, 'test', node['public'], self.localUserKey.getPrivateKey(), joined['shadowname'])

        if result['result'] == 'error':
            print(" ~~~ quota command FAILED ~~~ ")
            print(result['error'])
        else:
            if self.auth.verify_two_way_result(node['verify'], result):
                print(" *** quota *** ")
                print(self.auth.decrypt_two_way_result(result, self.localUserKey.getPrivateKey()))
            else:
                print(" ~~~ quota command FAILED ~~~ ")
                print(" Verifying signature failed ")

                return False

        return True

    def dir(self, nodes: Nodes, myNodes: MyNodes, node_name: str, filepath : str = '/'):
        myNode = myNodes.findNode(node_name)
        currentNode = nodes.findNode(node_name)    
        
        if currentNode == False:
            raise NodeNotFound(node_name)

        shadowname = myNode['shadowname']

        url = currentNode['url'] + "/files/list"

        result = self.auth.get_by_two_way_encryption(
            url, 
            'test', 
            currentNode['public'], 
            self.localUserKey.getPrivateKey(), 
            shadowname)

        if result['result'] == 'error':
            print(" ~~~ list command FAILED ~~~ ")
            print(result['error'])
        else:
            if self.auth.verify_two_way_result(currentNode['verify'], result):
                print(" *** list *** ")
                files = json.loads(
                    self.auth.decrypt_two_way_result(
                        result, 
                        self.localUserKey.getPrivateKey()))['files']

                print(files)
            else:
                print(" ~~~ list command FAILED ~~~ ")
                print(" Verifying signature failed ")

                return False

        return True

    def upload(self, nodes: Nodes, myNodes: MyNodes, node_name: str, filepath: str):
        myNode = myNodes.findNode(node_name)
        currentNode = nodes.findNode(node_name)    
        filename = os.path.basename(filepath)  
        
        if currentNode == False:
            raise NodeNotFound(node_name)

        shadowname = myNode['shadowname']

        url = currentNode['url'] + "/files/touch"

        result = self.auth.get_by_two_way_encryption(
            url, 
            'test', 
            currentNode['public'], 
            self.localUserKey.getPrivateKey(), 
            shadowname, 
            {'filename': self.auth.encrypt(filename, currentNode['public'])})
        
        if result['result'] == 'error':
            print(" ~~~ touch command FAILED ~~~ ")
            print(result['error'])
        else:
            if self.auth.verify_two_way_result(currentNode['verify'], result):
                print(" *** File touch *** ")

                fileinfo = json.loads(self.auth.decrypt_two_way_result(
                    result, 
                    self.localUserKey.getPrivateKey()))

                uploaded = fileinfo['size']
                file_size = os.path.getsize(filepath)

                if uploaded >= file_size:
                    print (" *** Olready uploaded *** ")
                    return True

                blocks = math.ceil((file_size - uploaded) / self.block_size)
                url = currentNode['url'] + "/files/append/" + fileinfo['id']

                file = open(filepath, "rb")
                
                print("Uploading file ...", flush=True)

                for i in range(blocks):
                    file.seek(uploaded + (self.block_size * i))
                    data = file.read(self.block_size)

                    result = self.auth.post_data_by_auth_id(
                        data, 
                        url, 
                        self.localUserKey.getPrivateKey(), 
                        currentNode['url'], 
                        currentNode['nonce'], 
                        self.localUserKey.getUsername(), 
                        shadowname, 
                        self.localUserKey.getNonce())

                    if result['result'] == 'error':
                        print("")
                        print(" ~~~ Upload failed ~~~ ")
                        print(result['error'])
                        return False
                    else:
                        print("+", end = " ", flush=True)

                file.close()

                print ()
                print (" *** UPLOADED *** ")
            else:
                print(" ~~~ list command FAILED ~~~ ")
                print(" Verifying signature failed ")

                return False

        return True

    def fileinfo(self, nodes: Nodes, myNodes: MyNodes, node_name: str, file_id: str):
        myNode = myNodes.findNode(node_name)
        currentNode = nodes.findNode(node_name) 
        
        if currentNode == False:
            raise NodeNotFound(node_name)

        shadowname = myNode['shadowname']

        url = currentNode['url'] + "/files/fileinfo"

        result = self.auth.get_by_two_way_encryption(
            url, 'test', 
            currentNode['public'], 
            self.localUserKey.getPrivateKey(), 
            shadowname, 
            {'file_id': file_id})

        if result['result'] == 'error':
            print(" ~~~ fileinfo command FAILED ~~~ ")
            print(result['error'])
        else:
            if self.auth.verify_two_way_result(currentNode['verify'], result):

                fileinfo = json.loads(self.auth.decrypt_two_way_result(result, self.localUserKey.getPrivateKey()))

                fileinfo['dl'] = currentNode['url'] + "/files/download/" + shadowname + "/" + fileinfo['id'] + "/" + self.auth.auth_id(self.localUserKey.getPrivateKey(), currentNode['url'], currentNode["nonce"], self.localUserKey.getUsername(), self.localUserKey.getNonce())

                fileinfo['pub'] = currentNode['url'] + "/files/pub/" + fileinfo['id'] + "-" + shadowname + "-" + self.auth.alternative_id(self.localUserKey.getPrivateKey(), currentNode['url'], currentNode["nonce"], self.localUserKey.getUsername(), self.localUserKey.getNonce())

                return fileinfo
            else:
                print(" ~~~ fileinfo command FAILED ~~~ ")
                print(" Verifying signature failed ")

                return False

        return True

    def quota(self, nodes: Nodes, myNodes: MyNodes, node_name: str):
        myNode = myNodes.findNode(node_name)
        currentNode = nodes.findNode(node_name) 
        
        if currentNode == False:
            raise NodeNotFound(node_name)

        shadowname = myNode['shadowname']

        url = currentNode['url'] + "/files/quota"

        result = self.auth.get_by_two_way_encryption(url, 'test', currentNode['public'], self.localUserKey.getPrivateKey(), shadowname)

        if result['result'] == 'error':
            print(" ~~~ quota command FAILED ~~~ ")
            print(result['error'])
        else:
            if self.auth.verify_two_way_result(currentNode['verify'], result):
                print(" *** quota *** ")
                print(self.auth.decrypt_two_way_result(result, self.localUserKey.getPrivateKey()))
            else:
                print(" ~~~ quota command FAILED ~~~ ")
                print(" Verifying signature failed ")

                return False

        return True

    def download(self, nodes: Nodes, myNodes: MyNodes, node_name: str, file_id: str):
        myNode = myNodes.findNode(node_name)
        currentNode = nodes.findNode(node_name)    
        url_dl = currentNode['url'] + "/files/download/" + file_id
        
        if currentNode == False:
            raise NodeNotFound(node_name)

        shadowname = myNode['shadowname']

        fileinfo = self.fileinfo(nodes, myNodes, node_name, file_id)

        # url_dl = currentNode['url']\
        #     + "/files/download/"\
        #     + shadowname\
        #     + "/"\
        #     + fileinfo['id']\
        #     + "/"\
        #     + self.auth.auth_id(
        #         self.localUserKey.getPrivateKey(), 
        #         currentNode['url'], 
        #         currentNode["nonce"], 
        #         self.localUserKey.getUsername(), 
        #         self.localUserKey.getNonce())

        filename = fileinfo['filename']
        size = fileinfo['size']

        f = open(filename, 'ab')
        pos = f.tell()
        # print(pos)

        headers = {'Range': 'bytes=' + str(pos) + '-'}

        responce = self.auth.get_responce_by_auth_id(
            url_dl, 
            self.localUserKey.getPrivateKey(), 
            currentNode['url'], 
            currentNode['nonce'], 
            self.localUserKey.getUsername(), 
            shadowname, 
            self.localUserKey.getNonce(), 
            headers)
        # print(responce.status_code)
        for block in responce.iter_content(chunk_size = self.block_size):
            f.write(block)
            print("+", end = " ", flush=True)

        f.close()

        print("")
        print(" *** DOWNLOAD OK *** ")

        return True

    def remove(self, username: str, node_url: str, file_id: str):
        myNode = myNodes.findNode(node_name)
        currentNode = nodes.findNode(node_name)    
        filename = os.path.basename(filepath)  
        
        if currentNode == False:
            raise NodeNotFound(node_name)

        shadowname = myNode['shadowname']

        url = currentNode['url'] + "/files/touch"

        joined = self.joined(username, node_url)

        if joined == False:
            return False

        result = ness_auth.get_by_two_way_encryption(url, 'test', currentNode['public'], self.localUserKey.getPrivateKey(), joined['shadowname'], 
            {'file_id': file_id})
        
        if result['result'] == 'error':
            print(" ~~~ remove command FAILED ~~~ ")
            print(result['error'])
        else:
            if ness_auth.verify_two_way_result(node['verify'], result):
                print(" *** File removed *** ")
            else:
                print(" ~~~ list command FAILED ~~~ ")
                print(" Verifying signature failed ")

                return False

        return True