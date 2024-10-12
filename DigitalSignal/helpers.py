import cmath


PI = cmath.pi


class E():
    """
    For use in signals where there is element-wise multiplication with e^(j*omega*n)
    E.g. y[n] = e^(j*pi*n) * x[n] becomes y = x * E(1j*PI), where y and x are instances of DigitalSignal  
    """

    def __init__(self, complex_const, ndigits=None):

        if isinstance(complex_const, complex) and complex_const.real != 0:
            raise TypeError("E can only take fully imagineary numbers (e.g. -2j not 3+4j)")

        self.imag_const = complex_const.imag
        self.ndigits = ndigits

    def __call__(self, value):

        z = cmath.cos(self.imag_const * value) + 1j * cmath.sin(self.imag_const * value)

        if self.ndigits is None:
            return z

        return  complex(round(z.real, self.ndigits), round(z.imag, self.ndigits))


def cconj(signal):
    """
    A helper function that calls the complex_conjugate method on a DigitalSignal object
    """

    try:
        return signal.complex_conjugate() 
    except AttributeError:
        raise AttributeError