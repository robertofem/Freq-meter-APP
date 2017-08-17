#!/usr/bin/env python3
# Standard libraries
import os
import socket
import yaml

class FreqMeterDevice(object):
    """Class for working with a frequency meter instrument"""
    _COMMANDS = {
        "ack": "*IDN?",
        "init": "INIT",
        "reset": "*RST",
        "set_freq_coarse": "SENS:FREQ:COARSE:ARM:TIM",
        "set_freq_fine": "SENS:FREQ:FINE:ARM:TIM",
        "set_freq_fineCDT": "SENS:FREQ:FINECDT:ARM:TIM",
        "set_freq_all": "SENS:FREQ:ALL:ARM:TIM",
        "fetch_coarse": "FETCH:FREQ:COARSE?",
        "fetch_fine": "FETCH:FREQ:FINE?",
        "fetch_fineCDT": "FETCH:FREQ:FINECDT?",
        "fetch_all": "FETCH:ALL?",
    }
    def __init__(self, dev_path, logger):
        self.logger = logger
        # Communications socket for a TCP/IP communication.
        self._client = None
        self._connected = False
        self._ack = False
        self._timeout = 0.2
        # Read and load the device configuration file
        self._dev_path = dev_path
        with open(self._dev_path, 'r') as read_file:
            self._dev_data = yaml.load(read_file)
        # Load the device communication configured protocol.
        self._comm_protocol = self._dev_data['communications']['Protocol']
        # If the protocol is 'TCP/IP', prepare a network socket.
        if self._comm_protocol == "TCP/IP":
            self._client = socket.socket(family=socket.AF_INET,
                                         type=socket.SOCK_STREAM)
            self._client.settimeout(self._timeout)

    def send_command(self, command, arg=""):
        """
        Send a command with an optional argument and return response.

        The client will read the response message until a limit of 100
        characters are read or a timeout exception raises (which
        indicates that the server is not returning more values).
        """
        if not self._connected:
            self.logger.warn("Device not connected")
            return
        cmd = self._COMMANDS[command]
        if arg:
            cmd = "{} {}".format(cmd, arg)
        message = ""
        self.logger.debug("Sending '{}' to server".format(cmd))
        self._client.send(str.encode(cmd))
        # Read back the answer from the server.
        try:
            message = self._client.recv(100)
        except socket.timeout:
            pass
        self.logger.debug("Received '{}'".format(message))
        return message

    def connect(self):
        """
        Try to connect to the device. Return True if sucessfull.

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
            self.logger.debug("Conecting to IP {} and port {}".format(ip, port))
            self._client = socket.socket(family=socket.AF_INET,
                                         type=socket.SOCK_STREAM)
            self._client.settimeout(self._timeout)
            try:
                self._client.connect((ip, port))
            except (socket.timeout, ConnectionRefusedError) as error:
                self._client.close()
                self._connected = False
                self._ack = False
            else:
                self._connected = True
        else:
            self._connected = False
            self._ack = False
            self.logger.warn("Unable to work with specified protocol '{}'"
                        "".format(self._comm_protocol))
        return (self._connected, self._ack)

    def connect_and_ack(self):
        """
        Open the socket connection and if succesfull, send an ACK.
        """
        # Try to connect and to get an acknowledge.
        connected = self.connect()
        ack = self.acknowledge()
        dev_name = self._dev_data['general']['Name']
        # Evaluate the connection state and send to logger information
        if connected and ack:
            self.logger.info("{}: Established connection to target "
                             "device".format(dev_name))
        elif connected and not ack:
            self.logger.warn("{}: Established connection to target device,"
                             " but no ACK received".format(dev_name))
        else:
            self.logger.warn("{}: Unable to connect to device. {}."
                            "".format(dev_name, error))
        return (self._connected, self._ack)

    def disconnect(self):
        """Disconnect from the device server."""
        if self._comm_protocol == "TCP/IP":
            if self._connected:
                self._client.send(b"EXIT")
                self._client.close()
                self.logger.info("{}: Closed the TCP/IP client."
                            "".format(self._dev_data['general']['Name']))
                self._connected = False
            else:
                self.logger.warn("{}: Unable to close TCP/IP client. Already"
                        " closed".format(self._dev_data['general']['Name']))
        return self._connected

    def acknowledge(self):
        """
        Send the ACK command for checking if the device is correct.

        This is used to check that the client has been connected to the
        correct server, which implements the same communications
        protocol.
        """
        message = self.send_command("ack")
        if message != "":
            self._ack = True
        return self._ack

    def is_connected(self):
        """Return the state of the connection."""
        return self._connected

    def is_ack(self):
        """Return the state of the acknowledge."""
        return self._ack
