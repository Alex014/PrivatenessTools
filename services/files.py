from NessKeys.keys.MyNodes import MyNodes
from NessKeys.keys.Nodes import Nodes
from NessKeys.keys.UserLocal import UserLocal
from NessKeys.keys.Directories import Directories as DirectoriesKey
from NessKeys.keys.Files import Files as FilesKey

from NessKeys.exceptions.NodeNotFound import NodeNotFound
from NessKeys.exceptions.NodeError import NodeError
from NessKeys.exceptions.AuthError import AuthError

import json
from ness.NessAuth import NessAuth
import math
import os
import requests
from prettytable import PrettyTable
import humanize

from NessKeys.CryptorMaker import CryptorMaker
from NessKeys.BlockCryptor import BlockCryptor
from NessKeys.interfaces.output import output as ioutput

class files:
    cipher_type = 'salsa20'
    block_size = 1024**2

    def __init__(self, localUserKey: UserLocal, nodes: Nodes, myNodes: MyNodes, filesKey: FilesKey, directoriesKey: DirectoriesKey, output: ioutput):
        self.localUserKey = localUserKey
        self.nodes = nodes
        self.myNodes = myNodes

        self.node_name = self.myNodes.getCurrentNode()

        self.auth = NessAuth()

        self.filesKey = filesKey
        self.directoriesKey = directoriesKey

        self.output = output


    def dir(self):
        myNode = self.myNodes.findNode(self.node_name)
        currentNode = self.nodes.findNode(self.node_name)    
        
        if currentNode == False:
            raise NodeNotFound(self.node_name)

        shadowname = myNode['shadowname']

        url = currentNode['url'] + "/files/list"

        result = self.auth.get_by_two_way_encryption(
            url, 
            'test', 
            currentNode['public'], 
            self.localUserKey.getPrivateKey(), 
            shadowname)

        if result['result'] == 'error':
            self.err = result['error']
        else:
            if self.auth.verify_two_way_result(currentNode['verify'], result):
                files = json.loads(
                    self.auth.decrypt_two_way_result(
                        result, 
                        self.localUserKey.getPrivateKey()))['files']

                return files
            else:
                self.err = " Verifying signature failed "

                return False

        return True

    def upload(self, filepath: str, file_shadowname: str):
        myNode = self.myNodes.findNode(self.node_name)
        currentNode = self.nodes.findNode(self.node_name) 
        filename = os.path.basename(filepath)  
        
        if currentNode == False:
            raise NodeNotFound(self.node_name)

        shadowname = myNode['shadowname']

        url = currentNode['url'] + "/files/touch"

        result = self.auth.get_by_two_way_encryption(
            url, 
            'test', 
            currentNode['public'], 
            self.localUserKey.getPrivateKey(), 
            shadowname, 
            {'filename': self.auth.encrypt(file_shadowname, currentNode['public'])})
        
        if result['result'] == 'error':
            self.output.line(" ~~~ touch command FAILED ~~~ ")
            self.output.line(result['error'])
        else:
            if self.auth.verify_two_way_result(currentNode['verify'], result):
                self.output.line(" *** File touch *** ")

                fileinfo = json.loads(self.auth.decrypt_two_way_result(
                    result, 
                    self.localUserKey.getPrivateKey()))

                uploaded = fileinfo['size']
                file_size = os.path.getsize(filepath)

                if uploaded >= file_size:
                    self.output.line (" *** Olready uploaded *** ")
                    return True

                blocks = math.ceil((file_size - uploaded) / self.block_size)
                url = currentNode['url'] + "/files/append/" + fileinfo['id']
                # self.output.line(fileinfo)

                file = open(filepath, "rb")
                
                self.output.line("Uploading file from " + filepath)

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
                        self.output.line("")
                        self.output.line(" ~~~ Upload failed ~~~ ")
                        self.output.line(result['error'])
                        return False
                    else:
                        self.output.out("+")

                file.close()

                self.output.line ('')
                self.output.line (" *** UPLOADED *** ")
                self.output.line ("File shadowname: " + file_shadowname)
            else:
                self.output.line(" ~~~ list command FAILED ~~~ ")
                self.output.line(" Verifying signature failed ")

                return False

        return True

    def __fileinfo(self, file_id: str):
        myNode = self.myNodes.findNode(self.node_name)
        currentNode = self.nodes.findNode(self.node_name) 
        
        if currentNode == False:
            raise NodeNotFound(self.node_name)

        shadowname = myNode['shadowname']

        url = currentNode['url'] + "/files/fileinfo"

        result = self.auth.get_by_two_way_encryption(
            url, 'test', 
            currentNode['public'], 
            self.localUserKey.getPrivateKey(), 
            shadowname, 
            {'file_id': file_id})

        if result['result'] == 'error':
            self.output.line(" ~~~ fileinfo command FAILED ~~~ ")
            self.output.line(result['error'])
        else:
            if self.auth.verify_two_way_result(currentNode['verify'], result):

                fileinfo = json.loads(self.auth.decrypt_two_way_result(result, self.localUserKey.getPrivateKey()))

                fileinfo['dl'] = currentNode['url'] + "/files/download/" + shadowname + "/" + fileinfo['id'] + "/" + self.auth.auth_id(self.localUserKey.getPrivateKey(), currentNode['url'], currentNode["nonce"], self.localUserKey.getUsername(), self.localUserKey.getNonce())

                fileinfo['pub'] = currentNode['url'] + "/files/pub/" + fileinfo['id'] + "-" + shadowname + "-" + self.auth.alternative_id(self.localUserKey.getPrivateKey(), currentNode['url'], currentNode["nonce"], self.localUserKey.getUsername(), self.localUserKey.getNonce())

                return fileinfo
            else:
                self.output.line(" ~~~ fileinfo command FAILED ~~~ ")
                self.output.line(" Verifying signature failed ")

                return False

        return True

    def fileinfo(self, shadowname: str):
        dir = self.dir()
        info_node = self. __fileinfo(dir[shadowname]['id'])
        info_local = self.filesKey.getFiles(self.node_name)[shadowname]

        fileinfo = {
            'id': info_node['id'],
            'filename': info_local['filename'],
            'cipher': info_local['cipher'],
            'shadowname': shadowname,
            'status': self.__status(info_local['status']),
            'size_local': info_local['size'],
            'size_remote': humanize.naturalsize(info_node['size']),
            'filepath': info_local['filepath'],
            'pub': info_node['pub']
        }

        if fileinfo['size_local'] != '':
            fileinfo['size_local'] = humanize.naturalsize(fileinfo['size_local'])

        return fileinfo

    def quota(self):
        myNode = self.myNodes.findNode(self.node_name)
        currentNode = self.nodes.findNode(self.node_name) 
        
        if currentNode == False:
            raise NodeNotFound(self.node_name)

        shadowname = myNode['shadowname']

        url = currentNode['url'] + "/files/quota"

        result = self.auth.get_by_two_way_encryption(url, 'test', currentNode['public'], self.localUserKey.getPrivateKey(), shadowname)

        if result['result'] == 'error':
            self.output.line(" ~~~ quota command FAILED ~~~ ")
            self.output.line(result['error'])
        else:
            if self.auth.verify_two_way_result(currentNode['verify'], result):
                self.output.line(" *** quota *** ")
                self.output.line(self.auth.decrypt_two_way_result(result, self.localUserKey.getPrivateKey()))
            else:
                self.output.line(" ~~~ quota command FAILED ~~~ ")
                self.output.line(" Verifying signature failed ")

                return False

        return True

    def __download(self, file_id: str, real_filename: str, path: str = ''):
        myNode = self.myNodes.findNode(self.node_name)
        currentNode = self.nodes.findNode(self.node_name)    
        url_dl = currentNode['url'] + "/files/download/" + file_id
        
        if currentNode == False:
            raise NodeNotFound(self.node_name)

        shadowname = myNode['shadowname']

        fileinfo = self.__fileinfo(file_id)

        filename = fileinfo['filename']

        if path != '':
            if path[-1] != '/':
                path = path + '/'
            filename = path + filename
            real_filename = path + real_filename

        size = fileinfo['size']

        f = open(filename, 'ab')
        pos = f.tell()
        # self.output.line(pos)

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
        # self.output.line(responce.status_code)
        for block in responce.iter_content(chunk_size = self.block_size):
            f.write(block)
            self.output.out("+")

        f.close()

        os.rename(filename, real_filename)

        self.output.line("")
        self.output.line(" *** DOWNLOAD OK *** ")

        return True

    def __remove(self, file_id: str):
        myNode = self.myNodes.findNode(self.node_name)
        currentNode = self.nodes.findNode(self.node_name)
        
        if currentNode == False:
            raise NodeNotFound(self.node_name)

        shadowname = myNode['shadowname']

        url = currentNode['url'] + "/files/remove"

        result = self.auth.get_by_two_way_encryption(
            url, 
            'test', 
            currentNode['public'], 
            self.localUserKey.getPrivateKey(), 
            shadowname,
            {'file_id': file_id})
        
        if result['result'] == 'error':
            self.output.line(" ~~~ remove command FAILED ~~~ ")
            self.output.line(result['error'])
        else:
            if self.auth.verify_two_way_result(currentNode['verify'], result):
                self.output.line(" *** File removed *** ")
                return True
            else:
                self.output.line(" ~~~ remove command FAILED ~~~ ")
                self.output.line(" Verifying signature failed ")

                return False


    def download(self, shadowname: str, path: str = ''):
        file = self.filesKey.getFile(self.node_name, shadowname)
        dir = self.dir()

        if shadowname in dir:

            if file['cipher-type'] != '':          
                decr_path = os.getcwd() + '/encrypted/'
                self.__download(dir[shadowname]['id'], file['filename'], decr_path)
            else:
                self.__download(dir[shadowname]['id'], file['filename'], path)

            return True
        else:
            return False


    def remove(self, shadowname: str):
        dir = self.dir()

        if shadowname in dir:
            self.__remove(dir[shadowname]['id'])
            return True
        else:
            return False


    def removeLocal(self, shadowname: str):
        file = self.filesKey.getFile(self.node_name, shadowname)
        if os.path.exists(file['filepath']):
            os.remove(file['filepath'])

    def __status(self, s: chr):
        if s == 'c':
            return 'Created'
        elif s == 'e':
            return 'Encrypting'
        elif s == 'u':
            return 'Uploading'
        elif s == 'n':
            return 'On Node'
        elif s == 'w':
            return 'Downloading'
        elif s == 'd':
            return 'Decrypting'


    def ls(self):
        myNode = self.myNodes.findNode(self.node_name)
        currentNode = self.nodes.findNode(self.node_name)
        currentDir = self.directoriesKey.getCurrentDir(self.node_name)
        
        if currentNode == False:
            raise NodeNotFound(self.node_name)

        node_shadowname = myNode['shadowname']

        dir = self.dir()

        if dir != False:
            t = PrettyTable(['Shadowname', 'Filename', 'Size', 'Cipher', 'Status', 'Filepath'])
            t.align = 'l'
            files = self.filesKey.getFiles(self.node_name, currentDir)
            directories = self.directoriesKey.ls(self.node_name)
            
            for id in directories:
                t.add_row([id, '[' + directories[id]['name'] + ']', '', '', '', ''])

            for shadowname in files:
                ffl = files[shadowname]
                if shadowname in dir:
                    dirf = dir[shadowname]

                    # pub = currentNode['url'] + "/files/pub/" + dirf['id'] + "-" + node_shadowname + "-" + self.auth.alternative_id(self.localUserKey.getPrivateKey(), currentNode['url'], currentNode["nonce"], self.localUserKey.getUsername(), self.localUserKey.getNonce())

                    t.add_row([shadowname, ffl['filename'], humanize.naturalsize(dirf['size']), ffl['cipher-type'], self.__status(ffl['status']), ffl['filepath']])
                else:
                    t.add_row([shadowname, ffl['filename'], '-', ffl['cipher-type'], self.__status(ffl['status']), ffl['filepath']])

            self.output.line(" *** Contents of {}: {}  ".format(currentDir, self.directoriesKey.path(self.node_name)))
            self.output.line(t)
        else:
            self.output.line(" ~~~ list command FAILED ~~~ ")
            self.output.line(self.err)


    def raw(self):
        dir = self.dir()

        if dir != False:
            t = PrettyTable(['Filename', 'ID', 'Size'])
            t.align = 'l'
            self.output.line(" *** list *** ")
            
            for file in dir:
                t.add_row([file, dir[file]['id'], dir[file]['size']])

            t.align = 'l'
            self.output.line(t)
        else:
            self.output.line(" ~~~ list command FAILED ~~~ ")
            self.output.line(self.err)


    def encrypt(self, filepath: str, shadowname: str):
        file = self.filesKey.getFile(self.node_name, shadowname)
        cryptor = CryptorMaker.make(file['cipher-type'])

        filename = os.path.basename(filepath)
        filename_out = os.getcwd() + '/encrypted/' + filename
        
        bc = BlockCryptor(cryptor, bytes(file['cipher'][:cryptor.getBlockSize()], 'utf8'), self.output, self.block_size)

        self.output.line("Encrypting file from {} to {}".format(filepath, filename_out))
        bc.encrypt(filepath, filename_out)
        self.output.line ("")
        self.output.line (" *** ENCRYPTED *** ")

        return filename_out


    def decrypt(self, shadowname: str, path: str = ''):
        file = self.filesKey.getFile(self.node_name, shadowname)
        dir = self.dir()

        if shadowname in dir:
            cryptor = CryptorMaker.make(file['cipher-type'])            
            
            decr_path = os.getcwd() + '/encrypted/'

            if path != '' and path[-1] != '/':
                path = path + '/'

            from_filename = decr_path + file['filename']
            to_filename = path + file['filename']
            
            bc = BlockCryptor(cryptor, bytes(file['cipher'][:cryptor.getBlockSize()], 'utf8'), self.output, self.block_size)

            self.output.line("Decrypting file from {} to {}".format(from_filename, to_filename))
            bc.decrypt(from_filename, to_filename)
            self.output.line ("")
            self.output.line (" *** DECRYPTED *** ")
            
            os.remove(from_filename)

            return True
        else:
            return False
