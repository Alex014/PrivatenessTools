from NessKeys.interfaces.NessKey import NessKey
from NessKeys.keys.NessFile import NessFile
from NessKeys.exceptions.LeafBuildException import LeafBuildException
from NessKeys.exceptions.FileNotExist import FileNotExist

import math
import random
import time
import os

class Files(NessKey):

    def __init__(self, keydata: dict):
        
        if not("filedata" in keydata):
            raise LeafBuildException("No filedata parameter", "/filedata")
            
        filedata = keydata["filedata"]

        if not ("vendor" in filedata and "type" in filedata and "for" in filedata):
            raise LeafBuildException("No vendor|type|for in filedata parameter", "/filedata/*")

        if not (filedata["vendor"] == "Privateness" and filedata["type"] == "service" and filedata["for"] == "files"):
            raise LeafBuildException("Wrong filetype", "/filedata/*")

        if not (isinstance(keydata["files"], dict)):
            raise LeafBuildException("Wrong files type", "/files")

        self.__files = keydata["files"]

    def compile(self) -> dict:
        appdata = {
            "filedata": {
                "vendor": "Privateness",
                "type": "service",
                "for": "files"
            },
            "files": self.__files
        }

        return appdata

    def worm(self) -> str:
        return ""
        
    def nvs(self) -> str:
        return ""

    def print(self):
        return "Privateness Files storage file"

    def filename():
        return "files.json"

    def getFilename(self):
        return "files.json"
        
    def getAllFiles(self, node_name: str):
        return self.__files[node_name]

        
    def getFiles(self, node_name: str, directory: int):
        fl = {}

        for shadowname in self.__files[node_name]:
            if int(self.__files[node_name][shadowname]['directory']) == directory:
                fl[shadowname] = self.__files[node_name][shadowname]

        return fl

    def getFile(self, node_name: str, shadowname: str) -> dict:
        if not node_name in self.__files:
            return False

        if not shadowname in self.__files[node_name]:
            return False

        return self.__files[node_name][shadowname]

    def getFileByFilename(self, node_name: str, filename: str):
        for fl in self.__files[node_name]:
            if fl['filenname'] == filename:
                return fl

        return False

    def removeFile(self, node_name: str, shadowname: str):
        if shadowname in self.__files[node_name]:
            del self.__files[node_name][shadowname]

    def __gen_shadowname(self):
        alphabet_1 = ('q','w','r','t','y','p','s','d','f','g','h','k','l','z','x','c','v','b','n','m')
        alphabet_2 = ('e','u','i','o','a')

        random.seed(time.time())
        rand = math.floor(random.uniform(11, 99))

        return random.choice(alphabet_1) + \
            random.choice(alphabet_1) + \
            random.choice(alphabet_1) + \
            random.choice(alphabet_2) + '.' + str(rand)

    def addFile(self, node_name: str, filepath: str, cipher: str, cipher_type: str, status: chr, directory: int) -> str:
        shadowname = self.__gen_shadowname()
        filename = os.path.basename(filepath)

        self.__files[node_name][shadowname] = {
            'filename': filename,
            'filepath': filepath,
            'cipher': cipher,
            'size': os.path.getsize(filepath),
            'cipher-type': cipher_type,
            'status': status,
            'directory': directory
        }

        return shadowname

    def initFiles(self, node_name: str):
        if not node_name in self.__files:
            self.__files[node_name] = {}

    def setFileName(self, node_name: str, shadowname: str, filename: str):
        if not shadowname in self.__files[node_name]:
            raise FileNotExist(shadowname)

        self.__files[node_name][shadowname]['filename'] = filename

    def setFileStatus(self, node_name: str, shadowname: str, status: chr):
        if not shadowname in self.__files[node_name]:
            raise FileNotExist(shadowname)

        self.__files[node_name][shadowname]['status'] = status

        if 'paused' in self.__files[node_name][shadowname]:
            del self.__files[node_name][shadowname]['paused']


    def setFilePaused(self, node_name: str, shadowname: str):
        if not shadowname in self.__files[node_name]:
            raise FileNotExist(shadowname)

        self.__files[node_name][shadowname]['paused'] = True

    def setFileDirectory(self, node_name: str, shadowname: str, directory: int):
        if not shadowname in self.__files[node_name]:
            raise FileNotExist(shadowname)

        self.__files[node_name][shadowname]['directory'] = directory

    def setFilePath(self, node_name: str, shadowname: str, path: str):
        if not shadowname in self.__files[node_name]:
            raise FileNotExist(shadowname)

        self.__files[node_name][shadowname]['filepath'] = path

    def clearFilePath(self, node_name: str, shadowname: str):
        if not shadowname in self.__files[node_name]:
            raise FileNotExist(shadowname)

        self.__files[node_name][shadowname]['filepath'] = ''
        self.__files[node_name][shadowname]['size'] = ''
