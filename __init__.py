class RegisteredPath():
    path = None
    func = None

    def __init__(self, path, func):
        self.path = path
        self.func = func
    
    def Run(self, requestMessage):
        self.func(requestMessage)

class Server():
    ipAddress = "127.0.0.1"
    port = 80

    registeredPaths = []

    def __init__(self):
        pass

    def Listen(self):
        pass

    def Register(self, path, func):
        self.registeredPaths.append(RegisteredPath(path, func))
    
    def GetRegisteredPaths(self):
        return self.registeredPaths
