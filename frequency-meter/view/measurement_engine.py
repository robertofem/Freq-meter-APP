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

    def start(self, instr_list, fetch_time, sample_time):
        """
        Start periodic measurements with the instruments specified

        instr_list: list with the instruments to do the measurements.
        fetch_time: period in seconds to ask data to the instruments
        sample_time: gate_time or time used by the instrument to calculate
            one measurement, in seconds
        """
        # Generate a clean internal device list without Nones in it
        self._instr_list = []
        for instrument in instr_list:
            if instrument != None:
                self._instr_list.append(instrument)

        # Generate data structures to store measurements
        self._unsent_values = []
        for instrument in self._instr_list:
            self._unsent_values.append(
            instrument_data.InstrumentData(
                1,
                instrument.n_signals,
                instrument.sig_types
            ))

        # Tell the instruments to start measuring
        for instrument in self._instr_list:
            instrument.start_measurement(sample_time, 0)

        # Create a measurement timer object
        self._mtimer = MeasurementTimer(self._instr_list, fetch_time)
        # Create a signal/slot connection to start/stop the timer
        self._startTimer.connect(self._mtimer.start)
        self._stopTimer.connect(self._mtimer.stop)
        # Create a signal/slot connection to receive new samples from the thread
        self._mtimer.sampleReady.connect(self._new_samples)

        # Move the measurement timer to a new thread if threaded type requested
        if self.__threaded:
            self._thread = QtCore.QThread()
            self._mtimer.moveToThread(self._thread)
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

    def _new_samples(self, new_samples):
        """
        Function executed when new samples are available.
        new_samples: list of InstrumentData objects. Ech object contains
        only one sample for the instrument (last sample) for all channels and
        signals
        """
        # for each instrument
        for index in range(len(self._instr_list)):
            self._unsent_values[index].append(new_samples[index])
            print("new sample{}={}".format(index, new_samples[index]))
        return

    def get_values(self):
        """
        Retrieve measurements from the measurement engine. Values in the list
        unsent_values are given as return. unsent_values is cleared.
        """
        # Deep copy is used to copy lists containing objects
        return_values = copy.deepcopy(self._unsent_values)
        for unsent in self._unsent_values:
            unsent.clear()
        return return_values


class MeasurementTimer(QtCore.QObject):
    """
    Implements a timer that periodically asks a new sample from instruments.
    Inherit from QObject to be able to use Qt signals
    It contains the sampleReady signal that emits every time a new sample is
    received from instruments
    """
    # Signals (must be non-dynamic class members):
    # Flags to the main thread that new samples from instruments are available
    sampleReady = QtCore.pyqtSignal(list)

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
