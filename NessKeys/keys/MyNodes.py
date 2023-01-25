from NessKeys.interfaces.NessKey import NessKey
from NessKeys.exceptions.LeafBuildException import LeafBuildException

class MyNodes(NessKey):

    def __init__(self, keydata: dict):
        
        if not("filedata" in keydata):
            raise LeafBuildException("No filedata parameter", "/filedata")
            
        filedata = keydata["filedata"]

        if not ("vendor" in filedata and "type" in filedata and "for" in filedata):
            raise LeafBuildException("No vendor|type|for in filedata parameter", "/filedata/*")

        if not (filedata["vendor"] == "Privateness" and filedata["type"] == "service" and filedata["for"] == "node"):
            raise LeafBuildException("Wrong filetype", "/filedata/*")

        if not(type(keydata["my-nodes"]) == dict):
            raise LeafBuildException("Wrong my-nodes type", "/my-nodes")

        if not(keydata["current-node"] in keydata["my-nodes"]):
            raise LeafBuildException("current-node is not in nodes list", "/current-node")

        self.__current_node = keydata["current-node"]
        self.__my_nodes = keydata["my-nodes"]

    def compile(self) -> dict:
        appdata = {
            "filedata": {
                "vendor": "Privateness",
                "type": "service",
                "for": "node"
            },
            "my-nodes": self.__my_nodes,
            "current-node": self.__current_node,
        }

        return appdata

    def worm(self) -> str:
        return ""
        
    def nvs(self) -> str:
        return ""

    def print(self):
        return "Privateness User Nodes"

    def filename():
        return "my-nodes.json"

    def getFilename(self):
        return MyNodes.filename()

    def getCurrentNode(self) -> str:
        return self.__current_node

    def findNode(self, node_name: str):
        if node_name in self.__my_nodes:
            return self.__my_nodes[node_name]
        else:
            return False

    def changeCurrentNode(self, node_name: str) -> bool:
        if node_name in self.__my_nodes:
            self.__current_node = node_name
            return True
        else:
            return False

    def addNode(self, url: str, user_shadowname: str):
        self.__my_nodes[url] = {'shadowname': user_shadowname}

    def updateNode(self, url: str, user_shadowname: str):
        self.__my_nodes[url].update({'shadowname': user_shadowname})

    def removeNode(self, url: str):
        del self.__my_nodes[url]
