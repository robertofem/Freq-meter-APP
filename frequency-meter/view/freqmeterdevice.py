#!/usr/bin/env python3
# Standard libraries
import abc
import logging
import random
import yaml

# Local application
from view import clientprotocol


logger = logging.getLogger("view")


class FreqMeter(abc.ABC):
    @staticmethod
    def get_freq_meter(dev_path):
        with open(dev_path, 'r') as read_file:
            data = yaml.load(read_file)
            vendor = data["general"]["Vendor"]
        if vendor == "Uvigo":
            return UviFreqMeter(dev_path)
        elif vendor == "Agilent":
            return AgilentFreqMeter(dev_path)
        elif vendor == "Test":
            return TestFreqMeter(dev_path)
        else:
            return None

    def __init__(self, dev_path):
        # Read and load the device configuration file
        with open(dev_path, 'r') as read_file:
            self._dev_data = yaml.load(read_file)
        # Communication
        self.__client = clientprotocol.Client.get_client(
                self._dev_data['communications'])
        self.__connected = False

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

    def _send(self, cmd, read=False):
        success = self.__client.write(cmd)
        if success and read:
            return self.__client.read()
        else:
            return success, ""

    def is_connected(self):
        """Return the state of the connection."""
        return self.__connected

    def is_ready(self):
        success, _ = self.idn()
        return success

    def idn(self):
        return self._send("*IDN?", True)

    def reset(self):
        return self._send("*RST")

    @abc.abstractmethod
    def start_measurement(self, sample_time, channel):
        return

    @abc.abstractmethod
    def fetch_freq(self):
        return


class UviFreqMeter(FreqMeter):
    n_channels = 1
    n_signals = 3
    sig_types = {'S1': 'coarse', 'S2': 'fine', 'S3': 'fineCDT'}

    def start_measurement(self, sample_time, channel):
        self.reset()
        self._send("SENS:MODE:SAVELAST", True)
        self._send("SENS:FREQ:ALL:ARM:TIM {}".format(sample_time), True)
        self._send("INIT", True)

    def fetch_freq(self):
        success, reply = self._send("FETCH:FREQ:ALL", True)
        if not success:
            logger.error("Couldn't fetch frequency")
            return
        values = reply.decode().split(",")
        return {
            self.sig_types['S1']: float(values[0]),
            self.sig_types['S2']: float(values[1]),
            self.sig_types['S3']: float(values[2]),
        }

    def cdt_start(self, gate_time, number_of_measurements):
        self._send("CDT:ARM:TIM {},{}".format(gate_time,
                                              number_of_measurements),
                   True)

    def cdt_end(self):
        success, reply = self._send("CDT:END?")
        if not success:
            return None

        status = {
            "end": False,
            "error": False,
            "time_left": {
                "minutes": 0,
                "seconds": 0,
            },
        }
        if reply == "YES":
            status["end"] = True
        elif reply == "ERROR":
            status["error"] = True
        elif reply == "NOTSTARTED":
            pass
        else:
            time_values = reply.split(" ")[1]
            time_values = time_values.split(",")
            status["time_left"]["minutes"] = int(time_values[0])
            status["time_left"]["seconds"] = int(time_values[1])
        return status

    def cdt_get_values(self):
        values = {}
        success, reply = self._send("CDT:CDT?", True)
        if success:
            values["cdt"] = float(reply)
        success, reply = self._send("CDT:DNL?", True)
        if success:
            values["dnl"] = float(reply)
        success, reply = self._send("CDT:INL?", True)
        if success:
            values["inl"] = float(reply)
        return values


class AgilentFreqMeter(FreqMeter):
    n_channels = 2
    n_signals = 1
    sig_types = {'S1': 'fineCDT'}

    def start_measurement(self, sample_time, channel):
        self.reset()
        self._send("*CLS")
        self._send("*SRE 0")
        self._send("*ESE 0")
        self._send(":STAT:PRES")
        self._send(":FREQ:ARM:STAR:SOUR IMM")
        self._send(":FREQ:ARM:STOP:SOUR TIM")
        self._send(":FREQ:ARM:STOP:TIM {}".format(sample_time))
        self._send(":FUNC 'FREQ {}".format(channel+1))
        self._send("INIT")

    def fetch_freq(self):
        success, reply = self._send("FETC:FREQ?", True)
        if not success:
            logger.error("Couldn't fetch frequency")
            return
        return {
            self.sig_types['S1']: float(reply),
        }


class TestFreqMeter(FreqMeter):
    n_channels = 2
    n_signals = 3
    sig_types = {'S1': 'coarse', 'S2': 'fine', 'S3': 'fineCDT'}

    def start_measurement(self, sample_time, channel):
        return

    def fetch_freq(self):
        values = []
        for index in range(3):
            values.append(random.gauss(10, 1+index))
        return {
            self.sig_types['S1']: float(values[0]),
            self.sig_types['S2']: float(values[1]),
            self.sig_types['S3']: float(values[2]),
        }
