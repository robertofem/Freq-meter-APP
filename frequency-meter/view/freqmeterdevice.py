#!/usr/bin/env python3
# Standard libraries
import abc
from collections import OrderedDict
import datetime
import logging
import random
# Third party libraries
import yaml
# Local application
from view import clientprotocol


logger = logging.getLogger("view")


class FreqMeter(abc.ABC):
    @staticmethod
    def get_vendors():
        vendors = {}
        for freq_meter_class in FreqMeter.__subclasses__():
            vendors[freq_meter_class.get_vendor_name()] = {
                "channels": freq_meter_class.get_channels(),
                "signals": freq_meter_class.get_signals(),
                "protocols": freq_meter_class.get_protocols(),
                "impedances": freq_meter_class.get_impedances(),
            }
        return vendors

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

    @staticmethod
    @abc.abstractmethod
    def get_vendor_name():
        return ""

    @staticmethod
    @abc.abstractmethod
    def get_channels():
        return 0

    @staticmethod
    @abc.abstractmethod
    def get_signals():
        return []

    @staticmethod
    @abc.abstractmethod
    def get_protocols():
        return []

    @staticmethod
    @abc.abstractmethod
    def get_impedances():
        return []

    def __init__(self, dev_path):
        # Read and load the device configuration file
        with open(dev_path, 'r') as read_file:
            self._dev_data = yaml.load(read_file)
        # Communication
        self.__client = clientprotocol.Client.get_client(
                self._dev_data['communications'])
        self.__connected = False
        self._active_channel = None
        self._measurement_data = None

    def __init_measurement_data(self):
        measurement_data = []
        for _ in range(self.get_channels()):
            signal_measurements = OrderedDict()
            measurement_data.append(signal_measurements)
        return measurement_data

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
        self._measurement_data = self.__init_measurement_data()
        self._active_channel = channel
        return

    def store_freq(self):
        success, reply = self._fetch_freq()
        if not success:
            logger.error("Couldn't fetch frequency")
            return
        fetch_time = datetime.datetime.now()
        logger.info("Fetch time: {}".format(
                fetch_time.strftime("%H:%M:%S.%f")))
        values = reply.split(",")
        values = [float(value) for value in values]
        signals = self.get_signals()
        measurement = {}
        for index, value in enumerate(values):
            measurement[signals[index]] = value
        self._measurement_data[self._active_channel][fetch_time] = measurement
        return

    @abc.abstractmethod
    def _fetch_freq(self):
        return False, ""

    def get_measurement_data(self):
        return self._measurement_data


class UviFreqMeter(FreqMeter):
    @staticmethod
    def get_vendor_name():
        return "Uvigo"

    @staticmethod
    def get_channels():
        return 1

    @staticmethod
    def get_signals():
        return ["coarse", "fine", "fineCDT"]

    @staticmethod
    def get_protocols():
        return ["TCP/IP"]

    @staticmethod
    def get_impedances():
        return ["50", "1M"]

    n_channels = 1
    n_signals = 3
    sig_types = {'S1': 'coarse', 'S2': 'fine', 'S3': 'fineCDT'}

    def start_measurement(self, sample_time, channel):
        super(UviFreqMeter, self).start_measurement(sample_time, channel)
        self.reset()
        self._send("SENS:MODE:SAVELAST", True)
        self._send("SENS:FREQ:ALL:ARM:TIM {}".format(sample_time), True)
        self._send("INIT", True)

    def _fetch_freq(self):
        return self._send("FETCH:FREQ:ALL", True)

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
    @staticmethod
    def get_vendor_name():
        return "Agilent"

    @staticmethod
    def get_channels():
        return 2

    @staticmethod
    def get_signals():
        return ["fineCDT"]

    @staticmethod
    def get_protocols():
        return ["VISA"]

    @staticmethod
    def get_impedances():
        return ["50", "1M"]

    n_channels = 2
    n_signals = 1
    sig_types = {'S1': 'fineCDT'}

    def start_measurement(self, sample_time, channel):
        super(AgilentFreqMeter, self).start_measurement(sample_time, channel)
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

    def _fetch_freq(self):
        return self._send("FETC:FREQ?", True)


class TestFreqMeter(FreqMeter):
    @staticmethod
    def get_vendor_name():
        return "Test"

    @staticmethod
    def get_channels():
        return 2

    @staticmethod
    def get_signals():
        return ["coarse", "fine", "fineCDT"]

    @staticmethod
    def get_protocols():
        return ["Test"]

    @staticmethod
    def get_impedances():
        return ["50", "1M"]

    n_channels = 2
    n_signals = 3
    sig_types = {'S1': 'coarse', 'S2': 'fine', 'S3': 'fineCDT'}

    def start_measurement(self, sample_time, channel):
        super(TestFreqMeter, self).start_measurement(sample_time, channel)
        return

    def _fetch_freq(self):
        values = []
        for index in range(3):
            values.append(random.gauss(10, 1+index))
        return True, "{},{},{}".format(values[0], values[1], values[2])
