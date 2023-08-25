from .enums import RequestType


class HTTPRequest:
    _responseWriter = None

    def __init__(self, httpMessage):
        pass


class RegisteredPath:
    _path = None
    _requestType = None
    _func = None

    def __init__(self, path, requestType, func):
        self._path = path
        self._requestType = requestType
        self._func = func

    def Execute(self, httpRequest):
        self._func(httpRequest)

    def GetPath(self):
        return self._path

    def GetType(self):
        return self._requestType


# TODO: Implement Less Rigid Path Matching
def MatchPath(path1, path2):
    if path1.path == path2.path:
        return True


class Server:
    _ipAddress = None
    _port = None

    _registeredPaths = []

    def __init__(self, ipAddress="127.0.0.1", port=80):
        self._ipAddress = ipAddress
        self._port = port

    def Listen(self):
        pass

    def Register(self, path, requestType, func):
        registeredPath = RegisteredPath(path, requestType, func)
        self._registeredPaths.append(registeredPath)

    def RequestHandler(self, httpMessage):
        for registeredPath in self._registeredPaths:
            if registeredPath.GetType() == httpMessage.GetType():
                if MatchPath(registeredPath.GetPath(), httpMessage.GetPath()):
                    httpRequest = HTTPRequest(httpMessage)
                    registeredPath.Execute(httpRequest)
