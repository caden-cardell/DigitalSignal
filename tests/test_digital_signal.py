import pytest
from DigitalSignal.digital_signal import DigitalSignal as DS, E, PI, cconj

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

def test_callable():
    signal = DS([1, 2, 3, 4])
    callable_op = lambda a: a * 2

    signal2 = signal * callable_op

    signal3 = DS([2, 4, 6, 8])
    
    assert signal2 == signal3

def test_complex():
    signal = DS([1j, 1, 2+2j, -1j])
    cc_signal = cconj(signal)

    signal2 = DS([-1j, 1, 2-2j, 1j])

    assert cc_signal == signal2

def test_e_pi_no_rounding():
    callable_op = E(1j*PI)

    assert callable_op(2) != callable_op(8)  

def test_e_pi_rounding():
    callable_op = E(1j*PI, ndigits=6)

    assert callable_op(2) == callable_op(8)  