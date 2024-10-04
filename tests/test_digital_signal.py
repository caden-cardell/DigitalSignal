# tests/test_digital_signal.py

import pytest
from DigitalSignal.digital_signal import DigitalSignal  # Assuming you have a class named DigitalSignal

def test_signal_dirac():
    signal = DigitalSignal([1])
    assert signal[:] == [[1]]
