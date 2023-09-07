import asyncio
from .enums import RequestType


class HTTPMessage:
    reader = None
    writer = None
    host = None
    tcpAddress = None
    contentLength = None
    userAgent = None
    path = None
    type = None
    version = None
    unhandledHeaders = {}

    def parseHeader(self, line):
        delimLocation = line.find(":")
        header = line[:delimLocation]
        value = line[delimLocation + 1 :]

        if value[0] == " ":
            value = value[1:]  # Checks for and removes the optional trailing space (https://datatracker.ietf.org/doc/html/rfc9112#name-field-syntax)

        match header:
            case "Host":
                self.host = value
            case "Content-Length":
                self.contentLength = value
            case "User-Agent":
                self.userAgent = value
            case _:
                self.unhandledHeaders[header] = value

    async def readLine(self):
        data = await self.reader.readline()
        line = data.decode()
        if line[-2] == "\r":
            line = line[:-2]
        return line

    # Parse HTTPMessage into class variables
    async def parse(self):
        startLine = await self.readLine()
        options = startLine.split(" ")

        if len(options) != 3:
            self.writer.close()  # We close the connection because it's not a valid HTTP Message
            return

        match options[0]:
            case "GET":
                self.type = RequestType.GET
            case "POST":
                self.type = RequestType.POST
            case "PUT":
                self.type = RequestType.PUT
            case _:
                self.type = RequestType.UNKNOWN
        
        self.path = options[1]
        self.verison = options[2]

        completed = False

        while not completed:
            line = await self.readLine()

            if line == "":
                completed = True
                break

            self.parseHeader(line)

    def GetPath(self):
        return self.path

    def GetType(self):
        return self.requestType

    def __init__(self, reader, writer):
        self.writer = writer  # Take in writer for sending response
        self.reader = reader
        self.tcpAddress = writer.get_extra_info("peername")


class TCPServer:
    port = None
    ip = None
    numberOfBytes = None  # Amount of bytes read by read function
    requestHandler = None

    def __init__(self, port=7007, ip="127.0.0.1", numberOfBytes=100):
        self.port = port
        self.ip = ip
        self.numberOfBytes = numberOfBytes

    async def handler(self, reader, writer):
        httpMessage = HTTPMessage(
            reader, writer
        )  # Create HTTPMessage class to parse packet

        await httpMessage.parse()

        self.requestHandler(httpMessage)

    async def listenInternal(self):
        server = await asyncio.start_server(self.handler, self.ip, self.port)
        print(",".join(str(sock.getsockname()) for sock in server.sockets))

        async with server:
            await server.serve_forever()

    def Listen(self, requestHandler):
        self.requestHandler = requestHandler
        asyncio.run(self.listenInternal())
