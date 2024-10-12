try:
    from DigitalSignal import DigitalSignal
except:
    # this is a hack to allow ShiftRegister to be used in the online REPL
    pass

class ShiftRegister:
    def __init__(self, length):
        self.shift_size = length

    def __call__(self, signal_length):
        """
        Generate a signal of the given length from this shift register object
        """

        # create a shift register of length 'shift_size' with a leading '1'
        internal_signal = DigitalSignal([1]) + DigitalSignal()(-(self.shift_size-1))

        # generate an output of length 'signal_length'
        while len(internal_signal) < (signal_length):
            
            # modulus 2 add
            new_value = internal_signal[0] ^ internal_signal[self.shift_size-1]
            
            # shift signal and append to end
            internal_signal = internal_signal(-1)
            internal_signal[0] = new_value

        # convert 0s to -1s
        internal_signal = 2 * internal_signal

        internal_signal = internal_signal * (lambda a : a - 1) # subtract 1 from all explicit elements in the signal

        # reverse the explicit signal
        return DigitalSignal(internal_signal[::-1])