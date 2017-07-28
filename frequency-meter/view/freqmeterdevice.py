#!/usr/bin/env python3
# Standard libraries
import os
import socket
import yaml

class FreqMeterDevice(object):
    """Class for working with a frequency meter instrument"""
    def __init__(self, dev_name):
        # Communications socket for a TCP/IP communication.
        self._client = None
        self._connected = False
        # Read and load the device configuration file
        dev_dir = "{}/resources/devices/".format(os.getcwd())
        self._conf_file = "{dir}{dev}.yml".format(dir=dev_dir, dev=dev_name)
        with open(self._conf_file, 'r') as read_file:
            self._dev_data = yaml.load(read_file)
        # Load the device communication configured protocol.
        self._comm_protocol = self._dev_data['communications']['Protocol']
        # If the protocol is 'TCP/IP', prepare a network socket.
        if self._comm_protocol == "TCP/IP":
            self._client = socket.socket(family=socket.AF_INET,
                                         type=socket.SOCK_STREAM)
            self._client.settimeout(1.0)

    def connect(self, logger):
        """
        Try to connect to the device, and return True if sucessfull.
        """
        if self._comm_protocol == "TCP/IP":
            ip = self._dev_data['communications']['Properties']['CommProp1']
            port = int(self._dev_data['communications']['Properties']
                                     ['CommProp2'])
            try:
                self._client.connect((ip, port))
                self._connected = True
            except socket.timeout:
                logger.warn("{}: Unable to connect to device. Timeout."
                            "".format(self._dev_data['general']['Name']))
                self._connected = False
            else:
                logger.info("{}: Established connection to target device."
                            "".format(self._dev_data['general']['Name']))
                self._connected = True
        else:
            logger.warn("Unable to work with specified protocol '{}'"
                        "".format(self._comm_protocol))
            self._connected = False
        return self._connected

    def disconnect(self, logger):
        """Disconnect from the device."""
        if self._comm_protocol == "TCP/IP":
            if not isinstance(self._client._sock, socket._closedsocket):
                self.close()
                logger.info("{}: Closed the TCP/IP client."
                            "".format(self._dev_data['general']['Name']))
                self._connected = False
            else:
                logger.debug("{}: Unable to close TCP/IP client. Already closed"
                             ".".format(self._dev_data['general']['Name']))
        return self._connected
