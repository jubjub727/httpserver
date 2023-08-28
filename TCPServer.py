import asyncio


class HTTPMessage:
    # Preassign variables
    packet = None
    writer = None
    message = None
    sections = None
    host = None
    argument = None
    requestType = None
    unknownList = []

    # Parse HTTPMessage into class variables
    def parse(self):
        self.message = self.packet.decode()
        self.lines = self.message.split("\r\n")  # Put each line into a list
        for line in self.lines:
            if line.__contains__("GET"):
                self.argument = "GET"
                self.requestType = line.replace("GET", "")
            elif line.__contains__(
                ": "
            ):  # The request is the only part without a colon
                typePos = 0  # The first item in the split string would be the type
                dataPos = 1  # The other item would be the data
                lineParts = line.split(": ")
                if lineParts[typePos] == "Host":
                    self.host = lineParts[dataPos]
                else:
                    self.unknownList.append(line)
            else:
                self.unknownList.append(line)

    def GetPath():
        pass

    def GetType():
        pass

    def __init__(self, packet, writer):
        self.writer = writer  # Take in writer for sending response
        self.packet = packet
        self.parse()


class TCPServer:
    port = None
    ip = None
    numberOfBytes = None  # Amount of bytes read by read function
    requestHandler = None

    def __init__(self, port=7007, ip="127.0.0.1", numberOfBytes=-1):
        self.port = port
        self.ip = ip
        self.numberOfBytes = numberOfBytes

    async def handler(self, reader, writer):
        packet = await reader.read(self.numberOfBytes)
        httpMessage = HTTPMessage(
            packet, writer
        )  # Create HTTPMessage class to parse packet
        self.requestHandler(httpMessage)

    async def listenInternal(self):
        server = await asyncio.start_server(self.handler, self.ip, self.port)
        print(",".join(str(sock.getsockname()) for sock in server.sockets))

        async with server:
            await server.serve_forever()

    def Listen(self, requestHandler):
        self.requestHandler = requestHandler
        asyncio.run(self.listenInternal())
