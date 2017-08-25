class InstrumentData():
    """
    Class representing data for one instrument
    """
    def __init__ (self, n_channels, n_signals, sig_types):
        """
        number_channels: int: number of channels of the device
        n_signals: int: number of signals per channel
        signal_types: dict : with signal types. example {'S1': 'Coarse',
        'S2': Fine, 'S3': 'FineCDT'}
        """
        self.channel = [] #list of ChannelData
        for n in range(n_channels):
            self.channel.append(ChannelData(n_signals, sig_types))
        return

    def append(self, channels_to_append):
        for ch_index in range(len(self.channel)):
            self.channel[ch_index].append(channels_to_append.channel[ch_index])
        return

    def clear(self):
        for ch in self.channel:
            ch.clear()
        return

class ChannelData():
    """
    Class representing data for one channel
    """
    def __init__ (self, n_signals, sig_types):
        """
        n_signals: int: number of signals per channel
        signal_types: dict : with signal types. example {'S1': 'coarse',
        'S2': fine, 'S3': 'fineCDT'}
        """
        #dict storing the measurments for each signal in one channel
        #format = {'signal_type':[], 'signal_type':[]}
        self.signal = {}

        for signal_index in range(n_signals):
            sig_type_key = "S{}".format(signal_index+1)
            sig_type = sig_types[sig_type_key]
            self.signal.update({sig_type:[]})
        return

    def append(self, signals_to_append):
        """
        Appends the measuerments in ChannelData into the this object

        signals_to_append: ChannelData object to append
        """
        for sigtype, values in self.signal.items():
            values.append(signals_to_append.signal[sigtype])
            print(self.signal)
        return

    def append_sample(self, measuremnt):
        """
        Appends one measuremnt to the measuremnts in the this object

        measuremnt: dict with the self.signal format of self.signal
        """
        for sigtype, values in self.signal.items():
            values.append(measuremnt[sigtype])
            print(self.signal)
        return

    def clear(self):
        for sigtype, values in self.signal.items():
            values.clear()
        return
