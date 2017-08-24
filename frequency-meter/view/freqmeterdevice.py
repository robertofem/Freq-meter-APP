#!/usr/bin/env python3
# Standard libraries
import abc
import yaml
from view import clientprotocol


class FreqMeter(abc.ABC):
    def __init__(self, dev_path, logger):
        self.logger = logger
        # Read and load the device configuration file
        with open(dev_path, 'r') as read_file:
            self._dev_data = yaml.load(read_file)
        # Communication
        client_properties = {
            "ip": self._dev_data['communications']['Properties']['CommProp1'],
            "port": int(self._dev_data['communications']['Properties']
                        ['CommProp2']),
        }
        self.__client = clientprotocol.Client.get_client("TCP",
                                                         client_properties)
        self.__connected = False
        # Load the device communication configured protocol.
        self._comm_protocol = self._dev_data['communications']['Protocol']

    def connect(self):
        """
        Try to connect to the device. Return True if successful.

        Depending on the selected communications protocol, the procedure
        varies considerably.

        NOTE: The only validated protocol is TCP/IP.
        """
        self.__connected = self.__client.connect()
        return self.__connected

    def disconnect(self):
        """Disconnect from the device server."""
        self.__connected = not self.__client.disconnect()
        return self.__connected

    def _send(self, cmd):
        return self.__client.send(cmd)

    def is_connected(self):
        """Return the state of the connection."""
        return self.__connected

    def is_ready(self):
        success, _ = self.idn()
        return success

    def idn(self):
        return self.__client.send("*IDN?")

    def reset(self):
        return self.__client.send("*RST")

    @abc.abstractmethod
    def start_measurement(self, sample_time, channel):
        return

    @abc.abstractmethod
    def fetch_freq(self):
        return


class UviFreqMeter(FreqMeter):
    def start_measurement(self, sample_time, channel):
        self.reset()
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
