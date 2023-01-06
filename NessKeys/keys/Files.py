from NessKeys.interfaces.NessKey import NessKey
from NessKeys.keys.NessFile import NessFile
from NessKeys.exceptions.LeafBuildException import LeafBuildException

class Files(NessKey):

    def __init__(self, keydata: dict):
        
        if not("filedata" in keydata):
            raise LeafBuildException("No filedata parameter", "/filedata")
            
        filedata = keydata["filedata"]

        if not ("vendor" in filedata and "type" in filedata and "for" in filedata):
            raise LeafBuildException("No vendor|type|for in filedata parameter", "/filedata/*")

        if not (filedata["vendor"] == "Privateness" and filedata["type"] == "application" and filedata["for"] == "privateness-tools"):
            raise LeafBuildException("Wrong filetype", "/filedata/*")

        if not(type(keydata["files"]) == 'dict'):
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

    def getFilename(self):
        return "files.json"
        
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
