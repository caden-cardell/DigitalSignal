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


def test_signal_set_item():
    signal = DS()

    signal[-4] = 1
    assert signal[:] == [1, 0, 0, 0, 0]

    signal[2] = 3
    assert signal[:] ==  [1, 0, 0, 0, 0, 0, 3]


def test_signal_time_shift():
    signal = DS([0, 1, 2, 3, 4, 5])

    signal2 = signal(-2)

    assert signal2[4] == 2


def test_signal_add():
    signal1 = DS([-2, -1, [0]])
    signal2 = DS([[0], 1, 2])
    signal3 = signal1 + signal2

    assert signal3[:] == [-2, -1, 0, 1, 2]


def test_signal_sub():
    signal1 = DS([-2, -1, [0]])
    signal2 = DS([[0], 1, 2])
    signal3 = signal1 - signal2

    assert signal3[:] == [-2, -1, 0, -1, -2]


def test_signal_mul():
    signal = DS([0, 1, 2])

    signal2 = 2 * signal
    signal3 = signal * 3

    assert signal2[:] == [0, 2, 4]
    assert signal3[:] == [0, 3, 6]


def test_signal_neg():
    signal = DS([0, 1, 2])

    signal2 = -signal

    assert signal2[:] == [0, -1, -2]


def test_signal_fold():
    signal = DS([-1, [0], 1, 2])

    signal2 = ~signal

    assert signal2[1] == -1
    assert signal2[0] == 0
    assert signal2[-1] == 1
    assert signal2[-2] == 2