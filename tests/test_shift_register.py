
import pytest
from DigitalSignal import DigitalSignal as DS, ShiftRegister as SR

def test_shift_register():

    reg = SR(4)
    generated_signal = reg(15)
    known_signal = DS([-1, -1, -1, 1, 1, 1, 1, -1, 1, -1, 1, 1, -1, -1, 1])

    assert generated_signal == known_signal