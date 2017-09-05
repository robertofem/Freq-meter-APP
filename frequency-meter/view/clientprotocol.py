# Standard libraries
import abc
import socket
# Third party libraries
import visa


class Client(abc.ABC):
    @staticmethod
    def get_client(communications):
        if communications["Protocol"] == "TCP/IP":
            return TCPIPClient(communications["Properties"]['CommProp1'],
                               communications["Properties"]['CommProp2'])
        elif communications["Protocol"] == "VISA":
            return VISAClient(communications["Properties"]['CommProp1'],
                              communications["Properties"]['CommProp2'],
                              communications["Properties"]['CommProp3'],
                              communications["Properties"]['CommProp4'])
        elif communications["Protocol"] == "Test":
            return TestClient()
        else:
            return None

    @abc.abstractmethod
    def connect(self):
        return False

    @abc.abstractmethod
    def disconnect(self):
        return False

    @abc.abstractmethod
    def write(self, cmd):
        return False

    @abc.abstractmethod
    def read(self):
        return ""


class TCPIPClient(Client):
    TIMEOUT = 0.2

    def __init__(self, ip, port):
        self.__ip = ip
        self.__port = int(port)
        self.__socket = None

    def connect(self):
        self.__socket = socket.socket(family=socket.AF_INET,
                                      type=socket.SOCK_STREAM)
        self.__socket.settimeout(self.TIMEOUT)
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

    def write(self, command):
        if not self.__socket:
            return False
        self.__socket.send(str.encode(command))
        return True

    def read(self):
        if not self.__socket:
            return False, ""
        # Read back the answer from the server.
        try:
            reply = self.__socket.recv(100)
        except socket.timeout:
            reply = ""
            success = False
        else:
            success = True
        return success, reply


class VISAClient(Client):
    def __init__(self, ethernet_board, host_ip, lan_device, gpib_address):
        self.__ethernet_board = ethernet_board
        self.__host_ip = host_ip
        self.__lan_device = lan_device
        self.__gpib_address = gpib_address
        self.__resource = None

    def connect(self):
        rm = visa.ResourceManager("@py")
        visa_address = 'TCPIP{}::{}::{},{}::INSTR'.format(
                self.__ethernet_board,
                self.__host_ip,
                self.__lan_device,
                self.__gpib_address
        )
        self.__resource = rm.open_resource(visa_address)
        return True

    def disconnect(self):
        self.__resource.close()
        self.__resource = None
        return True

    def write(self, command):
        self.__resource.write(command)
        return True

    def read(self):
        return True, self.__resource.read()


class TestClient(Client):
    def __init__(self):
        return

    def connect(self):
        return True

    def disconnect(self):
        return True

    def write(self, command):
        return True

    def read(self):
        return True, 0.0
