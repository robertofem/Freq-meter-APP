# Standard libraries
import copy
import logging
# Third party libraries
from PyQt5 import QtCore
# Local libraries
from view import instrument_data

logger = logging.getLogger("view")


class MeasurementEngine(QtCore.QObject):
    """
    Launches a timer and for every tick in the timer
    it ask data to the instruments and adds it to a list. When the user
    asks for data it provides the data still not read.
    The timer can be optionally launched in a different thread passing
    "THREADED" to the initialization function. A threaded timer should
    be less affected by the main thread and should produce more periodic
    sampling.
    Inheritance from QObject to be able to use Qt signals.
    """
    # Signals (must be non-dynamic class members):
    # Signal to start the timer inside the new thread
    _startTimer = QtCore.pyqtSignal()
    # Signal to stop the timer inside the new thread
    _stopTimer = QtCore.pyqtSignal()

    def __init__(self, threaded=False):
        """
        threaded = "THREADED": launches the timer in different thread.
        threaded = any other value or nothing: launches timer in current thread.
        """
        QtCore.QObject.__init__(self)
        self.__threaded = threaded
        self._timer = None
        self._thread = None

    def start(self, devices, fetch_time, sample_time):
        """
        Start periodic measurements with the instruments specified

        instr_list: list with the instruments to do the measurements.
        fetch_time: period in seconds to ask data to the instruments
        sample_time: gate_time or time used by the instrument to calculate
            one measurement, in seconds
        """
        # Generate a clean internal device list without Nones in it
        self.__devices = []
        for device in devices:
            self.__devices.append(device)

        # Tell the instruments to start measuring
        for instrument in self.__devices:
            # TODO [floonone-20170918] pass selected measuring parameters
            instrument.start_measurement(sample_time, 0, "1MΩ")

        # Create a measurement timer object
        self.__measurement = MeasurementTimer(self.__devices, fetch_time)
        # Create a signal/slot connection to start/stop the timer
        self._startTimer.connect(self.__measurement.start)
        self._stopTimer.connect(self.__measurement.stop)

        # Move the measurement timer to a new thread if threaded type requested
        if self.__threaded:
            self._thread = QtCore.QThread()
            self.__measurement.moveToThread(self._thread)
            self._thread.start(QtCore.QThread.HighestPriority)

        # Start the timer
        self._startTimer.emit()

        logger.debug("Start sampling every {} seconds".format(fetch_time))
        return

    def stop(self):
        """
        Stop making periodic measurements with the instruments.
        """
        # Stop timer
        self._stopTimer.emit()

        if self.__threaded and self._thread:
            # Tell the thread to end and wait for its actual end
            self._thread.exit()
            self._thread.wait()
            # Destroy the thread object
            self._thread = None

        logger.debug("Sampling finished")
        return


class MeasurementTimer(QtCore.QObject):
    """
    Implements a timer that periodically asks a new sample from instruments.
    Inherit from QObject to be able to use Qt signals
    It contains the sampleReady signal that emits every time a new sample is
    received from instruments
    """
    # Signals (must be non-dynamic class members):
    # Flags to the main thread that new samples from instruments are available

    def __init__(self, instr_list, fetch_time):
        super(MeasurementTimer, self).__init__()
        self.instr_list = instr_list
        self.fetch_time = fetch_time
        self.__timer = None
        self.__measurement_counter = 0
        return

    def start(self):
        """
        Initialize and starts the measurement timer
        """
        # Init measurement counter, skip first 2 measurements, they can be wrong
        self.__measurement_counter = -2

        # Create the timer to fetch measurements periodically
        self.__timer = QtCore.QTimer()
        self.__timer.setTimerType(QtCore.Qt.PreciseTimer)
        self.__timer.timeout.connect(self.__measure)
        self.__timer.start(self.fetch_time * 1000)
        return

    def stop(self):
        """
        Stop the measurement timer.
        """
        if self.__timer:
            self.__timer.stop()
            self.__timer = None
        self.__measurement_counter = 0
        return

    def __measure(self):
        """
        Function executed when the timer event rises.
        It asks a new sample to each instrument and sends them back to
        using a signal.
        """
        self.__measurement_counter += 1
        if self.__measurement_counter > 0:
            # Store new frequency values for each instrument
            for instrument in self.instr_list:
                instrument.store_freq()
        return
