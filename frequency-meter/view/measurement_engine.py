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
    It inherits from QObject to be able to emit signals between This
    bject living in the main thread and the child thread created inside.
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
        self.thread = MeasurementThread(fetch_time)
        #Create a signal/slot connection to end the thread from the main thread
        self.signal_end_thread = QtCore.SIGNAL()
        thread.connect(self, self.signal_end_thread, self.thread._end_thread)
        #Create a signal/slot to receive new samples fom thread
        self.connect(thread, thread.signal_new_samples, self._new_samples)

        #Start the thread
        self.thread.start()
        self.logger.debug("Start sampling every {} seconds".format(fetch_time))
        return

    def stop(self):
        '''
        Overloads MeasurementEngine.stop to add thread support
        '''
        #Tell the thread to end
        self.emit(self.signal_end_thread)
        #Wait for thread to really end
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


class MeasurementThread(QtCore.QThread):
    '''
    Thread of execution where the timer lives and where it performs the periodic
    fetch of measurements from instruments
    '''
    def __init__(self, instr_list, fetch_time):
        QtCore.QThread.__init__(self)
        self.instr_list = instr_list
        self.fetch_time = fetch_time
        #signal to send new samples (in dict form) back to main thread-safe
        self.signal_new_samples = QtCore.SIGNAL({})
        return

    def run(self):
        """
        Overload of the QThread.run() function. This is the function executed
        in a different thread when start() is executed from the main thread on
        a QThread object.
        """
        #create the timer to fetch measurements periodically
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._measure_thread)
        self.timer.start(self.fetch_time*1000)
        #Init measuremnt counter (skip first 2 measurements (they can be wrong))
        self.measurement_counter = -2

        #Wait until the main thread wants to end measurements
        self.finish = False
        while not self.finish:
            pass

        #Stop and destroy the timer
        self.timer.stop()
        self.timer = None

        #Destroy the thread (use wait after it to ensure it has finished)
        self.terminate()
        return

    def _measure_thread(self):
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
                    InstrumentData(
                        1,
                        self.instr_list[i].n_signals,
                        self.instr_list[i].signal_types
                    )
                )
                freq_val[i].channel[0].append_sample(
                    self.instr_list[i].fetch_freq()
                )
            #signal to the main thread so it can store the new samples
            self.emit(self.signal_new_samples, freq_vals)
        return

    def _end_thread(self):
        '''
        Slot to receive from the main thread that the measurement thread
        must be terminated
        '''
        self.finish = True
        return
