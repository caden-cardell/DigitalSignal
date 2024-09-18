from .digital_signal import DigitalSignal

# Define a function to make the module callable
def __call__(data):
    return DigitalSignal(data)