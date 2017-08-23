#!/usr/bin/env python3
# Standard libraries
import abc
import socket
import yaml


class FreqMeter(abc.ABC):
    def __init__(self, dev_path, logger):
        self.logger = logger
        # Communications socket for a TCP/IP communication.
        self._client = None
        self._connected = False
        # Read and load the device configuration file
        with open(dev_path, 'r') as read_file:
            self._dev_data = yaml.load(read_file)
        # Load the device communication configured protocol.
        self._comm_protocol = self._dev_data['communications']['Protocol']

    def _send(self, cmd):
        """
        Send a command with an optional argument and return response.

        The client will read the response message until a limit of 100
        characters are read or a timeout exception raises (which
        indicates that the server is not returning more values).
        """
        if not self._connected:
            self.logger.warn("Device not connected")
            return False, ""
        self.logger.debug("Sending '{}' to server".format(cmd))
        self._client.send(str.encode(cmd))
        # Read back the answer from the server.
        try:
            reply = self._client.recv(100)
            success = True
        except socket.timeout:
            reply = ""
            success = False
        self.logger.debug("Received '{}'".format(reply))
        return (success, reply)

    def connect(self):
        """
        Try to connect to the device. Return True if successful.

        Depending on the selected communications protocol, the procedure
        varies considerably.

        NOTE: The only validated protocol is TCP/IP.
        """
        if self._comm_protocol == "TCP/IP":
            ip = self._dev_data['communications']['Properties']['CommProp1']
            port = int(self._dev_data['communications']['Properties']
                                     ['CommProp2'])
            # If the connection fails, a new socket has to be created. This is
            # not the best solution. It is used to avoid BlockingIOError after
            # the first try. Other library like 'select' should be used.
            self.logger.debug("Connecting to IP {} and port {}".format(ip,
                                                                       port))
            self._client = socket.socket(family=socket.AF_INET,
                                         type=socket.SOCK_STREAM)
            self._client.settimeout(2)
            try:
                self._client.connect((ip, port))
            except (socket.timeout, ConnectionRefusedError) as error:
                self._client.close()
                self._connected = False
                connection_error = error
                self.logger.error("Unable to connect to device: '{}'".format(
                        connection_error))
            else:
                self._connected = True
                connection_error = None
        else:
            self._connected = False
            connection_error = "Unknown protocol"
            self.logger.warn("Unable to work with specified protocol '{}'"
                             "".format(self._comm_protocol))
        return (self._connected, connection_error)

    def disconnect(self):
        """Disconnect from the device server."""
        if self._comm_protocol == "TCP/IP":
            if self._connected:
                self._client.send(b"EXIT")
                self._client.close()
                self.logger.info("{}: Closed the TCP/IP client.".format(
                        self._dev_data['general']['Name']))
                self._connected = False
            else:
                self.logger.warn("{}: Unable to close TCP/IP client. Already"
                                 " closed".format(
                                    self._dev_data['general']['Name']))
        return self._connected

    def is_connected(self):
        """Return the state of the connection."""
        return self._connected

    def is_ready(self):
        success, _ = self.idn()
        return success

    def idn(self):
        return self._send("*IDN?")

    def reset(self):
        return self._send("*RST")

    @abc.abstractmethod
    def start_measurement(self, sample_time):
        return

    @abc.abstractmethod
    def fetch_freq(self):
        return


class UviFreqMeter(FreqMeter):
    def start_measurement(self, sample_time):
        self._send("*RST")
        self._send("SENS:MODE:SAVELAST")
        self._send("SENS:FREQ:ALL:ARM:TIM {}".format(sample_time))
        self._send("INIT")

    def fetch_freq(self):
        success, reply = self._send("FETCH:FREQ:ALL")
        if not success:
            self.logger.error("Couldn't fetch frequency")
            return
        values = reply.decode().split(",")
        return {
            "coarse": float(values[0]),
            "fine": float(values[1]),
            "fineCDT": float(values[2]),
        }
