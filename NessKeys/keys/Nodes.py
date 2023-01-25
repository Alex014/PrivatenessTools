from NessKeys.interfaces.NessKey import NessKey
from NessKeys.exceptions.LeafBuildException import LeafBuildException
from NessKeys.exceptions.MyNodesFileDoesNotExist import MyNodesFileDoesNotExist
from NessKeys.exceptions.CurrentNodeNotSet import CurrentNodeNotSet

class Nodes(NessKey):

    def __init__(self, keydata: dict):
        
        if not("filedata" in keydata):
            raise LeafBuildException("No filedata parameter", "/filedata")
            
        filedata = keydata["filedata"]

        if not ("vendor" in filedata and "type" in filedata and "for" in filedata):
            raise LeafBuildException("No vendor|type|for in filedata parameter", "/filedata/*")

        if not (filedata["vendor"] == "Privateness" and filedata["type"] == "data" and filedata["for"] == "nodes-list"):
            raise LeafBuildException("Wrong filetype", "/filedata/*")

        if not(type(keydata["nodes"]) == dict):
            raise LeafBuildException("Wrong my-nodes type", "/nodes")

        self.__nodes = keydata["nodes"]

    def compile(self) -> dict:
        appdata = {
            "filedata": {
                "vendor": "Privateness",
                "type": "data",
                "for": "nodes-list"
            },
            "nodes": self.__nodes
        }

        return appdata

    def worm(self) -> str:
        return ""
        
    def nvs(self) -> str:
        return ""

    def print(self):
        return "Privateness Nodes storage file"

    def filename():
        return "nodes.json"

    def getFilename(self):
        return Nodes.filename()

    def getNodes(self) -> dict:
        return self.__nodes

    def setNodes(self, nodes: dict):
        self.__nodes = nodes

    def findNode(self, node_name: str) -> dict:
        if node_name in self.__nodes:
            return self.__nodes[node_name]
        else:
            return False