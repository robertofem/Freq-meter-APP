# Standard libraries
import abc
import socket


class Client(abc.ABC):
    @abc.abstractmethod
    def connect(self):
        return False

    @abc.abstractmethod
    def disconnect(self):
        return False

    @abc.abstractmethod
    def send(self, cmd):
        return False, ""


class TCP(Client):
    def __init__(self, ip, port):
        self.__ip = ip
        self.__port = port
        self.__socket = None

    def connect(self):
        self.__socket = socket.socket(family=socket.AF_INET,
                                      type=socket.SOCK_STREAM)
        self.__socket.settimeout(2)
        try:
            self.__socket.connect((self.__ip, self.__port))
        except (socket.timeout, ConnectionRefusedError) as error:
            self.__socket.close()
            self.__socket = None
            return False

        return True

    def disconnect(self):
        if self.__socket:
            self.__socket.send(b"EXIT")
            self.__socket.close()
            self.__socket = None
        return True

    def send(self, command):
        if not self.__socket:
            return False, ""
        self.__socket.send(str.encode(command))
        # Read back the answer from the server.
        try:
            reply = self.__socket.recv(100)
            success = True
        except socket.timeout:
            reply = ""
            success = False
        return success, reply
