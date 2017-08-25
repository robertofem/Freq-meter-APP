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
        self.logger.debug("Sampling finished")
        return

    def get_values(self):
        """
        Retrieve measurements the measurement engine. Values in the queue
        unsent_values are given as return. unsent_values is cleared.
        """
        #deepcopy is used to copy lists containing objects
        return_values = copy.deepcopy(self.unsent_values)
        for unsent in self.unsent_values:
            unsent.clear()
        return return_values

    def _generate_internal_device_list(self, instrument_list):
        """
        Generate a clean internal device list without Nones in it
        """
        self.instrument_list = []
        for instrument in instrument_list:
            if instrument != None:
                self.instrument_list.append(instrument)
        return

    def _generate_data_structures(self):
        """
        Generate data structures to store measurements
        """
        self.unsent_values = []
        for instrument in self.instrument_list:
            self.unsent_values.append(
            instrument_data.InstrumentData(
                1,
                instrument.n_signals,
                instrument.sig_types
            ))

    def _start_instruments(self, sample_time):
        for instrument in self.instrument_list:
            instrument.start_measurement(sample_time, 1)
        return

    def _measure(self):
        """
        This function is called by the timer event. It retrieves measurements
        from instruments and store them in unsent_values queue.
        """
        self.measurement_counter += 1
        if self.measurement_counter > 0:
            for index in range(len(self.instrument_list)):
                freq_val = self.instrument_list[index].fetch_freq()
                self.unsent_values[index].channel[0].append_sample(freq_val)
        return

class MeasurementEngineThreaded(MeasurementEngine):
    """
    Launches a timer in different thread and for every tick in the timer
    it ask data to the instruments and adds it to a thread-safe queue.
    When the user asks for data from the main thread it reads the queue and
    provides the data still not read.
    """

    def __init__(self, logger):
        super(MeasurementEngineThreaded, self).__init__(logger)
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
        self.thread = threading.Thread(target=self._thread_function)
        self.fetch_time = fetch_time
        #Create variable to kill the thread and stop measurements
        self.thread_stop = threading.Event()
        self.thread_stop.clear()
        #Create some thread-safe FIFO queues to retrieve data from the Thread
        #Each Queue saves the values from one instrument
        #Each element of the Queue is a InstrumentData object containing
        #just one measurement
        self.data_queue = []
        for index in range(len(self.instrument_list)):
            self.data_queue.append(queue.Queue())

        #Start the thread
        self.thread.start()
        self.logger.debug("Start sampling every {} seconds".format(fetch_time))
        return

    def stop(self):
        '''
        Overloads MeasurementEngine.stop to add thread support
        '''
        #Tell the thread to stop
        self.thread_stop.set()
        #Wait for thread to really stop
        self.thread.join()
        self.thread = None
        return

    def _thread_function(self):
        #create the timer to fetch measurements periodically
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._measure)
        self.timer.start(self.fetch_time*1000)
        #Init measuremnt counter (skip first 2 measurements (they can be wrong))
        self.measurement_counter = -2

        #Wait until the main thread wants to end measurements
        while not self.thread_stop.isSet():
            pass
        #Stop and destroy the timer
        self.timer.stop()
        self.timer = None
        return

    def get_values(self):
        """
        Overload of MeasurementEngine.get_values to add thread support
        Retrieve measurements the measurement engine. Values in the
        thread-safe queue are retrieved and send to the user
        """
        for index in range(len(self.instrument_list)):#for each instrument
            #clear the measuremnts sent in previous call to the function
            self.unsent_values[index].clear()
            #copy values from thread-safe queue to unsent_values
            while not self.data_queue[index].empty():
                self.unsent_values[index].append(self.data_queue[index].get())
        return self.unsent_values

    def _measure(self):
        """
        Overload of MeasurementEngine.measure to add thread support.
        For every instrument it makes a mesurement and ads it to a thread-safe
        queue
        """
        self.measurement_counter += 1
        if self.measurement_counter > 0:
            for index in range(len(self.instrument_list)):#for each instrument
                freq_val = self.instrument_list[index].fetch_freq()
                freq_val_obj = InstrumentData(
                    1,
                    self.instrument_list[index].n_signals,
                    self.instrument_list[index].signal_types
                )
                freq_val_obj.append_sample(freq_val)
                self.data_queue[index].put(freq_val_obj)
        return
