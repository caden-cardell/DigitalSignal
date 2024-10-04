# tests/test_digital_signal.py

import pytest
from DigitalSignal.digital_signal import DigitalSignal as DS # Assuming you have a class named DigitalSignal

def test_signal_empty_initialization():
    signal = DS()
    assert signal[:] == [0]

def test_signal_dirac():
    signal = DS([1])
    assert signal[:] == [1]

def test_signal_get_item():
    signal = DS([1, 2, [3], 4, 5])

    assert signal[-100] == 0
    assert signal[-3] == 0
    assert signal[-2] == 1
    assert signal[-1] == 2
    assert signal[0] == 3
    assert signal[1] == 4
    assert signal[2] == 5
    assert signal[3] == 0
    assert signal[100] == 0

