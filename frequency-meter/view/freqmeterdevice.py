#!/usr/bin/env python3
# Standard libraries
import os
import socket
import yaml

class FreqMeterDevice(object):
    """Class for working with a frequency meter instrument"""
    def __init__(self, dev_path, logger):
        self.logger = logger
        # Communications socket for a TCP/IP communication.
        self._client = None
        self._connected = False
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
            self._client.settimeout(0.5)

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
            try:
                self._client.connect((ip, port))
            except socket.timeout:
                self._client.close()
                self._connected = False
                self._client = socket.socket(family=socket.AF_INET,
                                             type=socket.SOCK_STREAM)
                self._client.settimeout(0.5)
                self.logger.warn("{}: Unable to connect to device. Timeout."
                            "".format(self._dev_data['general']['Name']))
            else:
                self._connected = True
                self.logger.info("{}: Established connection to target device."
                            "".format(self._dev_data['general']['Name']))
        else:
            self._connected = False
            self.logger.warn("Unable to work with specified protocol '{}'"
                        "".format(self._comm_protocol))
        return self._connected

    def disconnect(self):
        """Disconnect from the device."""
        if self._comm_protocol == "TCP/IP":
            if self._connected:
                self._client.close()
                self.logger.info("{}: Closed the TCP/IP client."
                            "".format(self._dev_data['general']['Name']))
                self._connected = False
            else:
                self.logger.warn("{}: Unable to close TCP/IP client. Already"
                        " closed".format(self._dev_data['general']['Name']))
        return self._connected

    def is_connected(self):
        """Return the state of the connection."""
        return self._connected
