from PyQt5 import QtCore
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
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.measure)
        self.logger = logger
        return

    def start(self, instrument_list, fetch_time, sample_time):
        """
        Start measurements with the instruments specified

        instr_paths: list with paths of instruments to do the measurements.
        fetch_time: period in seconds to ask data to the instruments
        sample_time: gate_time or time used by the instrument to calculate
            one measurement
        """

        #Generate a clean list
        self.instrument_list = []
        for instrument in instrument_list:
            if instrument != None:
                self.instrument_list.append(instrument)

        #Create data structures for each device and start measurements
        self.unsent_values = []
        for instrument in self.instrument_list:
            self.unsent_values.append(
            instrument_data.InstrumentData(
                1,
                instrument.n_signals,
                instrument.sig_types
            ))
            instrument.start_measurement(sample_time, 1)

        #start the timer
        self.measurement_counter = -2  #slip first 2 measurements (can be wrong)
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

    def measure(self):
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
