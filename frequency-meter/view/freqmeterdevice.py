#!/usr/bin/env python3
# Standard libraries
import abc
import yaml
from view import clientprotocol


class FreqMeter(abc.ABC):
    @staticmethod
    def get_freq_meter(dev_path, logger):
        with open(dev_path, 'r') as read_file:
            data = yaml.load(read_file)
            vendor = data["general"]["Vendor"]
        if vendor == "Uvigo":
            return UviFreqMeter(dev_path, logger)
        elif vendor == "Agilent":
            return AgilentFreqMeter(dev_path, logger)
        else:
            return None

    def __init__(self, dev_path, logger):
        self.logger = logger
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
    def start_measurement(self, sample_time, channel):
        self.reset()
        self._send("SENS:MODE:SAVELAST", True)
        self._send("SENS:FREQ:ALL:ARM:TIM {}".format(sample_time), True)
        self._send("INIT", True)

    def fetch_freq(self):
        success, reply = self._send("FETCH:FREQ:ALL", True)
        if not success:
            self.logger.error("Couldn't fetch frequency")
            return
        values = reply.decode().split(",")
        return {
            "coarse": float(values[0]),
            "fine": float(values[1]),
            "fineCDT": float(values[2]),
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
            values = reply.split(" ")
            status["time_left"]["minutes"] = int(values[1])
            status["time_left"]["seconds"] = int(values[2])
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
    def start_measurement(self, sample_time, channel):
        self.reset()
        self._send("*CLS")
        self._send("*SRE 0")
        self._send("*ESE 0")
        self._send(":STAT:PRES")
        self._send(":FREQ:ARM:STAR:SOUR IMM")
        self._send(":FREQ:ARM:STOP:SOUR TIM")
        self._send(":FREQ:ARM:STOP:TIM {}".format(sample_time))
        self._send(":FUNC 'FREQ {}".format(channel))
        self._send("INIT")

    def fetch_freq(self):
        success, reply = self._send("READ:FREQ?", True)
        if not success:
            self.logger.error("Couldn't fetch frequency")
            return
        return {
            "coarse": float(reply),
        }
