
import pytest
from DigitalSignal.digital_signal import DigitalSignal as DS, ShiftRegister as SR, E, PI

def test_shift_register():

    reg = SR(4)
    generated_signal = reg(15)
    known_signal = DS([-1, -1, -1, 1, 1, 1, 1, -1, 1, -1, 1, 1, -1, -1, 1])

    assert generated_signal == known_signal