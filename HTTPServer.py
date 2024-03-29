from .enums import RequestType
from .TCPServer import TCPServer


class HTTPRequest:
    _tcpServer = None
    _writer = None
    message = None

    def __init__(self, httpMessage, tcpServer):
        self.message = httpMessage
        self._writer = httpMessage.writer
        self._tcpServer = tcpServer

    async def Reply(self, httpResponse):
        await self._tcpServer.Reply(httpResponse, self._writer)


class RegisteredPath:
    _path = None
    _requestType = None
    _func = None

    def __init__(self, path, requestType, func):
        self._path = path
        self._requestType = requestType
        self._func = func

    async def Execute(self, httpRequest):
        await self._func(httpRequest)

    def GetPath(self):
        return self._path

    def GetType(self):
        return self._requestType


# TODO: Implement Less Rigid Path Matching
def MatchPath(path1, path2):
    if path1 == "" or path1 == "/":
        if path2 == "" or path2 == "/":
            return True
    elif path1 == path2:
        return True


class Server:
    _ipAddress = None
    _port = None
    _tcpServer = None

    _registeredPaths = []

    def __init__(self, port=80, ipAddress="127.0.0.1"):
        self._ipAddress = ipAddress
        self._port = port
        self._tcpServer = TCPServer(self._port, self._ipAddress, -1)

    def Listen(self):
        self._tcpServer.Listen(self.RequestHandler)

    def Register(self, path, requestType, func):
        registeredPath = RegisteredPath(path, requestType, func)
        self._registeredPaths.append(registeredPath)

    async def RequestHandler(self, httpMessage):
        for registeredPath in self._registeredPaths:
            if registeredPath.GetType() == httpMessage.type:
                if MatchPath(registeredPath.GetPath(), httpMessage.path):
                    httpRequest = HTTPRequest(httpMessage, self._tcpServer)
                    await registeredPath.Execute(httpRequest)
                    return
