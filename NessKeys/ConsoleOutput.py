from NessKeys.interfaces.output import output as ioutput

class ConsoleOutput (ioutput):
    def out (self, data):
        print(data, flush = True, end = '')

    def line (self, data):
        print(data, flush = True)