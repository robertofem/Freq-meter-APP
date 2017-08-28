from PyQt5 import QtCore
import queue
import threading
import copy

from view import freqmeterdevice
from view import instrument_data

class MeasurementEngine():
    """
    Launches a timer and for every tick in the timer
    it ask data to the instruments and adds it to a list. When the user
    asks for data it provides the data still not read.
    """

    def __init__(self, logger):
        self.logger = logger
        return

    def start(self, instr_list, fetch_time, sample_time):
        """
        Start measurements with the instruments specified

        instr_list: list with the instruments to do the measurements.
        fetch_time: period in seconds to ask data to the instruments
        sample_time: gate_time or time used by the instrument to calculate
            one measurement, in seconds
        """

        #Generate a clean device list and data structures to save measurments
        self._generate_internal_device_list(instr_list)
        self._generate_data_structures()
        self._start_instruments(sample_time)

        #Init measuremnt counter (skip first 2 measurements (they can be wrong))
        self.measurement_counter = -2

        #Create and start timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._measure)
        self.timer.start(fetch_time*1000)
        self.logger.debug("Start sampling every {} seconds".format(fetch_time))
        return

    def stop(self):
        """
        Stop the timer and therefore the measurements
        """
        self.timer.stop()
        self.timer = None
        self.logger.debug("Sampling finished")
        return

    def get_values(self):
        """
        Retrieve measurements from the measurement engine. Values in the list
        unsent_values are given as return. unsent_values is cleared.
        """
        #deepcopy is used to copy lists containing objects
        return_values = copy.deepcopy(self.unsent_values)
        for unsent in self.unsent_values:
            unsent.clear()
        return return_values

    def _generate_internal_device_list(self, instr_list):
        """
        Generate a clean internal device list without Nones in it
        """
        self.instr_list = []
        for instrument in instr_list:
            if instrument != None:
                self.instr_list.append(instrument)
        return

    def _generate_data_structures(self):
        """
        Generate data structures to store measurements
        """
        self.unsent_values = []
        for instrument in self.instr_list:
            self.unsent_values.append(
            instrument_data.InstrumentData(
                1,
                instrument.n_signals,
                instrument.sig_types
            ))

    def _start_instruments(self, sample_time):
        for instrument in self.instr_list:
            instrument.start_measurement(sample_time, 1)
        return

    def _measure(self):
        """
        This function is called by the timer event. It retrieves measurements
        from instruments and store them in unsent_values list.
        """
        self.measurement_counter += 1
        if self.measurement_counter > 0:
            for i in range(len(self.instr_list)):
                self.unsent_values[i].channel[0].append_sample(
                    self.instr_list[i].fetch_freq()
                )
        return

class ThreadedMeasurementEngine(MeasurementEngine, QtCore.QObject):
    """
    Launches a timer in different thread and for every tick in the timer
    it asks data to the instruments and sends this data back to the main
    thread in a thread-safe way using Qt signals and slots.
    When the user asks for data from the main thread it reads the list of
    unsent values and provides them to user.
    It inherits from MeasurementEngine to reuse some of its functions
    It inherits from QObject to use Qt signals
    """

    #signals (must be non-dynamic class members):
    #signal to start the timer inside the new thread
    startTimer = QtCore.pyqtSignal()

    def __init__(self, logger):
        super(ThreadedMeasurementEngine, self).__init__(logger)
        QtCore.QObject.__init__(self)
        return

    def start(self, instr_list, fetch_time, sample_time):
        '''
        Overloads MeasurementEngine.start to add thread support
        '''
        #Generate a clean device list and data structures to save measurments
        self._generate_internal_device_list(instr_list)
        self._generate_data_structures()

        #Tell the instruments to start measuring
        self._start_instruments(sample_time)

        #Create a thread where the timer will live
        self.thread = QtCore.QThread()
        self.measurement_timer = MeasurementTimer(self.instr_list, fetch_time)
        self.measurement_timer.moveToThread(self.thread)
        #Create a signal/slot connection to start the timer
        self.startTimer.connect(self.measurement_timer.startTimer)
        #Create a signal/slot connection to receive new samples from the thread
        self.measurement_timer.sampleReady.connect(self._new_samples)

        #Start the thread
        self.thread.start()
        #Start the timer
        self.startTimer.emit()
        self.logger.debug("Start sampling every {} seconds".format(fetch_time))
        return

    def stop(self):
        '''
        Overloads MeasurementEngine.stop to add thread support
        '''
        #Tell the thread to end and wait for its actual end
        self.thread.exit()
        self.thread.wait()
        #Destroy the thread object
        self.thread = None
        return

    def _new_samples(self, new_samples):
        '''
        Function executed when new samples are available from measuremnt thread
        new_samples: list of InstrumentData objects. Ech object contains
        only one sample for the instrument (last sample) for all channels and
        signals
        '''
        for index in range(len(self.instr_list)):#for each instrument
            self.unsent_values[index].append(new_samples[index])
        return


class MeasurementTimer(QtCore.QObject):
    '''
    Thread of execution where the timer lives and where it performs the periodic
    fetch of measurements from instruments
    Inherit from QObject to be able to use Qt signals
    '''
    #signals (must be non-dynamic class members):
    #flags to the main thread that new samples from instruments are available
    sampleReady = QtCore.pyqtSignal(list)

    def __init__(self, instr_list, fetch_time):
        super(MeasurementTimer,self).__init__()
        self.instr_list = instr_list
        self.fetch_time = fetch_time
        return

    def startTimer(self):
        """
        This function initializes and starts the timer
        """
        #Init measuremnt counter (skip first 2 measurements (they can be wrong))
        self.measurement_counter = -2

        #create the timer to fetch measurements periodically
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._measure)
        self.timer.start(self.fetch_time*1000)
        return

    def _measure(self):
        """
        Function executed when the timer event rises.
        It asks a new sample to each instrument and sends them back to
        the main thread using a signal.
        """
        self.measurement_counter += 1
        if self.measurement_counter > 0:
            #get new frequency values from instruments
            freq_vals = []
            for i in range(len(self.instr_list)):#for each instrument
                freq_vals.append(
                    instrument_data.InstrumentData(
                        1,
                        self.instr_list[i].n_signals,
                        self.instr_list[i].sig_types
                    )
                )
                freq_vals[i].channel[0].append_sample(
                    self.instr_list[i].fetch_freq()
                )
            #signal to the main thread so it can store the new samples
            self.sampleReady.emit(freq_vals)
        return
