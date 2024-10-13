import cmath


class DigitalSignal:
    def __init__(self, data=[0], shape=None):
        """
        Initialize the DigitalSignal with data, identifying the zero index by a list element.
        """
        # Ensure the zero_index is within the bounds of the data array
        
        if shape is not None:
            if not isinstance(shape, slice):
                raise TypeError("shape must be type slice.")

            if not isinstance(data, (int, float, complex)):
                raise TypeError("If shape is not None then data must be a single scalar.")
            
            shape.start, shape.stop

            self.positive_indices = [data for _ in range(0, shape.stop)]
            self.negative_indices = [data for _ in range(shape.start, 0)]  # index order doesn't matter because all elements are the same value
            
            return
            
        zero_index=0
        for ind, element in enumerate(data):
            if isinstance(element, list):
                zero_index=ind
                data[ind] = element[0]

        for element in data:
            if not isinstance(element, (int, float, complex)):
                raise TypeError("DigitalSignal values can only be scalars.")

        if len(data) > 0:
            if zero_index < 0 or zero_index >= len(data):
                raise ValueError("zero_index must be within the range of the data array.")
        else:
            if zero_index != 0:
                raise ValueError("zero_index must be within the range of the data array.")
        
        # Separate the data into positive and negative indices
        self.positive_indices = data[zero_index:]    # Values at 0 and positive indices
        self.negative_indices = data[:zero_index][::-1]  # Values at negative indices (reversed order)

    def __repr__(self):
        """
        Return the string representation of the DigitalSignal.
        """
        neg = self.negative_indices[:]
        neg.reverse()
        pos = self.positive_indices[:]
        string_of_list = f"{' '.join(map(str, neg))} [{pos[0]}] {' '.join(map(str, pos[1:]))}"
        return f"DigitalSignal({string_of_list.strip()})"

    def __len__(self):
        """
        Return the total length of the non-zero portion of the signal.
        """
        return len(self.negative_indices) + len(self.positive_indices)

    def __getitem__(self, index):
        """
        Get the signal value at the specified index.
        """

        if not isinstance(index, (int, slice)):
            raise TypeError("Indexing only supports integers and slices.")
        
        # Handle slicing
        if isinstance(index, slice):
            return self.__slice_getitem(index)

        if index >= 0:
            # If the index is non-negative, return from positive_indices if in range

            if index < len(self.positive_indices):
                value = self.positive_indices[index]
            else:
                value = 0

            return value
        
        else:
            # If the index is negative, return from negative_indices after flipping sign
            index = -index - 1  # Convert negative index to zero-based positive index for negative_indices
            if index < len(self.negative_indices):
                value = self.negative_indices[index] 
            else:
                value = 0

            return value

    def __setitem__(self, index, value):
        """
        Set the signal value at the specified index.
        """

        if not isinstance(index, int):
            raise TypeError("Indexing only supports integers.")

        if not isinstance(value, (int, float, complex)):
            raise TypeError("DigitalSignal values can only be scalars.")
        
        if index >= 0:
            # If the index is non-negative

            while index > len(self.positive_indices):
                self.positive_indices.append(self[len(self.positive_indices)])

            self.positive_indices.append(value)

        else:
            # If the index is negative
            index = -index - 1

            while index > len(self.negative_indices):
                self.negative_indices.append(self[-(len(self.negative_indices)+1)])

            self.negative_indices.append(value)

    def __call__(self, amount=0):
        """
        Return a time shifted copy of the signal by the specified amount.
        """

        if not isinstance(amount, int):
            raise TypeError("Time-shifting only supports integers.")

        # Create a clone of the current Signal object
        clone = DigitalSignal()
        clone.positive_indices = self.positive_indices[:]
        clone.negative_indices = self.negative_indices[:]

        if amount < 0:
            # Shift to the left (negative shift)
            amount = abs(amount)
            for _ in range(amount):
                if clone.negative_indices:
                    # Pop from the front of the negative list
                    value = clone.negative_indices.pop(0)
                    # Append to the front of the positive list
                    clone.positive_indices.insert(0, value)
                else:
                    # No more negative values to shift, just insert zeros
                    clone.positive_indices.insert(0, 0)
        elif amount > 0:
            # Shift to the right (positive shift)
            for _ in range(amount):
                if clone.positive_indices:
                    # Pop from the front of the positive list
                    value = clone.positive_indices.pop(0)
                    # Append to the front of the negative list
                    clone.negative_indices.insert(0, value)
                else:
                    # No more positive values to shift, just insert zeros
                    clone.negative_indices.insert(0, 0)
        
        if len(clone.positive_indices) == 0:
            clone.positive_indices.append(0)

        return clone

    def __add__(self, other):
        """
        Return the elementwise addition of this signal and another DigitalSignal alined at the zero index.
        """
        if not isinstance(other, DigitalSignal):
            raise TypeError("Addition is only supported between two DigitalSignal objects.")

        # Determine the maximum length of the positive and negative lists
        max_pos_length = max(len(self.positive_indices), len(other.positive_indices))
        max_neg_length = max(len(self.negative_indices), len(other.negative_indices))
        
        # Create new lists with the appropriate size, initialized to zero
        new_pos = [0] * max_pos_length
        new_neg = [0] * max_neg_length
        
        # Add the positive parts of the two signals
        for i in range(max_pos_length):
            val_self = self.positive_indices[i] if i < len(self.positive_indices) else 0
            val_other = other.positive_indices[i] if i < len(other.positive_indices) else 0
            new_pos[i] = val_self + val_other
        
        # Add the negative parts of the two signals
        for i in range(max_neg_length):
            val_self = self.negative_indices[i] if i < len(self.negative_indices) else 0
            val_other = other.negative_indices[i] if i < len(other.negative_indices) else 0
            new_neg[i] = val_self + val_other

        # Return a new Signal object with the summed lists
        clone = DigitalSignal()
        clone.positive_indices = new_pos
        clone.negative_indices = new_neg
        return clone

    def __sub__(self, other):
        """
        Return the elementwise subtraction of another DigitalSignal from this signal alined at the zero index.
        """
        if not isinstance(other, DigitalSignal):
            raise TypeError("Subtraction is only supported between two DigitalSignal objects.")
        
        # Multiply the 'other' signal by -1 and add it to the current signal
        return self.__add__(other * -1)

    def __mul__(self, other):
        """
        Return a new DigitalSignal scaled by the given scalar.
        """
        if not isinstance(other, (int, float, complex)) and not callable(other):
            raise TypeError("The scalar must be an integer, float, complex or callable.")

        # Return a new Signal object with the scaled lists
        clone = DigitalSignal()

        if callable(other):
            clone.positive_indices = [value * other(idx) for idx, value in enumerate(self.positive_indices)]
            clone.negative_indices = [value * other(-(idx+1)) for idx, value in enumerate(self.negative_indices)]
        else:
            clone.positive_indices = [value * other for value in self.positive_indices]
            clone.negative_indices = [value * other for value in self.negative_indices]

        return clone

    def __rmul__(self, other):
        """
        Support scalar multiplication from the right.
        """
        return self.__mul__(other)

    def __neg__(self):
        """
        Return the negation of the DigitalSignal.
        """
        return -1 * self
    
    def __invert__(self):
        """
        Return the time-reversed DigitalSignal.
        """
        inverse = DigitalSignal()
        inverse.positive_indices = self.negative_indices[:]
        inverse.positive_indices.insert(0, self.positive_indices[0])
        inverse.negative_indices = self.positive_indices[1:]

        return inverse
    
    def __matmul__(self, other):
        """
        Return the convolution of this signal with another DigitalSignal.
        """
        if not isinstance(other, DigitalSignal):
            raise TypeError("Convolution is only supported between two DigitalSignal objects.")

        # Determine the maximum lag value
        neg_n = len(other.negative_indices) + len(self.negative_indices)
        pos_n = len(self.positive_indices) + len(other.positive_indices)
        n_range = [i for i in range(-(neg_n), pos_n-1)]
    
        # Initialize a list for storing cross-correlation results
        conv = DigitalSignal()

        # Iterate over all possible lags
        for n in n_range:
            sum_conv = 0  # Initialize the cross-correlation sum for this lag
            
            # Compute cross-correlation for each lag by summing over all valid n
            for k in range(-len(self.negative_indices), len(self.positive_indices)):
                # Values of y[n] and x[n-l] 
                y_k = self[k]
                x_k_n = other[n - k]

                sum_conv += y_k * x_k_n  # Accumulate the sum

            # Append the computed correlation value for the current lag
            conv[n] = (sum_conv)

        return conv

    def __mod__(self, other):
        """
        Return the lag indexed correlation of this signal with another DigitalSignal.
        """
        if not isinstance(other, DigitalSignal):
            raise TypeError("Correlation is only supported between two DigitalSignal objects.")
        return self @ (~(other.complex_conjugate()))

    def __eq__(self, other):
        """
        Return True both signals are equivalent, return False if not equivalent. 
        """

        max_neg_len = max(len(self.negative_indices), len(other.negative_indices))
        max_pos_len = max(len(self.positive_indices), len(other.positive_indices))

        for idx in range(max_neg_len+2):
            if self[idx] != other[idx]:
                return False
                
        for idx in range(max_pos_len+2):
            if self[-idx] != other[-idx]:
                return False
            
        return True
       
    def complex_conjugate(self):

        new_pos = [n.conjugate() if isinstance(n, complex) else n for n in self.positive_indices]
        new_neg = [n.conjugate() if isinstance(n, complex) else n for n in self.negative_indices]

        clone = DigitalSignal()
        clone.positive_indices = new_pos
        clone.negative_indices = new_neg
        return clone        

    def __slice_getitem(self, s):
        """
        Helper function to access the signal in slices
        """
        start, stop, step = s.start, s.stop, s.step

        n_len = len(self.negative_indices)
        p_len = len(self.positive_indices)

        if step == None:
            step = 1

        if step >= 0:
            if start == None:
                start = -n_len
            if stop == None:
                stop = p_len
        else: 
            if start == None:
                start = (p_len-1)
            if stop == None:
                stop = -(n_len+1)

        return [self[idx] for idx in range(start, stop, step)]
    
    def round(self, ndigits=None):

        # Initialize empty lists to store the rounded values
        new_pos = []
        new_neg = []

        # Iterate over positive indices and round each element
        for n in self.positive_indices:
            if isinstance(n, complex):
                rounded_value = complex(round(n.real, ndigits), round(n.imag, ndigits))
                
                # clean up zero values
                if rounded_value.imag == 0:
                    rounded_value = rounded_value.real
                elif rounded_value.real == 0:
                    rounded_value = rounded_value.imag

            else:
                rounded_value = round(n, ndigits)
            new_pos.append(rounded_value)

        # Iterate over negative indices and round each element
        for n in self.negative_indices:
            if isinstance(n, complex):
                rounded_value = complex(round(n.real, ndigits), round(n.imag, ndigits))

                # clean up zero values
                if rounded_value.imag == 0:
                    rounded_value = rounded_value.real
                elif rounded_value.real == 0:
                    rounded_value = rounded_value.imag
                
            else:
                rounded_value = round(n, ndigits)
            new_neg.append(rounded_value)

        clone = DigitalSignal()
        clone.positive_indices = new_pos
        clone.negative_indices = new_neg
        return clone     
    
    def shape(self):
        start = -len(self.negative_indices)
        stop = len(self.positive_indices)

        return slice(start, stop)


