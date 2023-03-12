from NessKeys.interfaces.output import output as ioutput

class NullOutput (ioutput):
    def out (self, data):
        pass

    def line (self, data):
        pass