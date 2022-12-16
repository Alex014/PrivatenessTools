from NessKeys.interfaces.NessKey import NessKey
from NessKeys.keys.NessFile import NessFile
from NessKeys.exceptions.LeafBuildException import LeafBuildException

class PrivatenessTools(NessKey):

    def __init__(self, keydata: dict):
        
        if not("filedata" in keydata):
            raise LeafBuildException("No filedata parameter", "/filedata")
            
        filedata = keydata["filedata"]

        if not ("vendor" in filedata and "type" in filedata and "for" in filedata):
            raise LeafBuildException("No vendor|type|for in filedata parameter", "/filedata/*")

        if not (filedata["vendor"] == "Privateness" and filedata["type"] == "application" and filedata["for"] == "privateness-tools"):
            raise LeafBuildException("Wrong filetype", "/filedata/*")

        if not ("files" in keydata and "current-node" in keydata and "my-nodes" in keydata):
            raise LeafBuildException("Not all parameters in place", "/*")

        if not(type(keys["files"]) == 'dict'):
            raise LeafBuildException("Wrong files type", "/files")

        files = keydata["files"]

        if not(type(keys["my-nodes"]) == 'list'):
            raise LeafBuildException("Wrong my-nodes type", "/my-nodes")

        if not("current-node" in keys["my-nodes"]):
            raise LeafBuildException("current-node is not in my-nodes list", "/current-node")

        self.__files = keydata["files"]
        self.__current_node = keydata["current-node"]
        self.__my_nodes = keydata["my-nodes"]

    def compile(self) -> dict:
        appdata = {
            "filedata": {
                "vendor": "Privateness",
                "type": "application",
                "for": "uprivateness-tools"
            },
            "my-nodes": self.__my_nodes,
            "current-node": self.__current_node,
            "files": self.__files
        }

        return appdata

    def worm(self) -> str:
        return ""
        
    def nvs(self) -> str:
        return ""

    def print(self):
        return "Privateness Application  \"privateness-tools\""

    def getFilename(self):
        return "privateness-tools.json"
        
    def getFiles(self):
        if self.__current_node not in self.__files:
            self.__file[self.__current_node] = {}

        files = []

        for file in self.__file[self.__current_node]:
            files.append(NessFile(file))

        return files

    def getFile(self, filename: str) -> NessFile:
        file = self.__files[self.__current_node][filename]

        return NessFile(file)

    def addFile(self, filename: str, file: NessFile):
        if self.__current_node not in self.__files:
            self.__file[self.__current_node] = {}

        if filename not in self.__files:
            self.__files[self.__current_node][filename] = NessFile.compile()

    def removeFile(self, filename: str):
        if filename in self.__files:
            del self.__files[self.__current_node][filename]

    def getMyNodes(self) -> list:
        return self.__my_nodes

    def getCurrentNode(self) -> str:
        return self.__current_node

    def changeNode(self, new_node: str) -> bool:
        if self.__my_nodes.count(new_node) > 0:
            self.__current_node = new_node
            return True
        else:
            return False

    def addNode(self, url: str):
        self.__my_nodes.append(url)

        if url in self.__files:
            self.__files[url] = {}

    def removeNode(self, url: str):
        self.__my_nodes.remove(url)
        del self.__files[self.__current_node]
