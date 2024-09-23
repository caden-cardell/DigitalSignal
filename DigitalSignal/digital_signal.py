
class DigitalSignal:
    def __init__(self, data=[0]):
        """
        Initialize the DigitalSignal with data, identifying the zero index by a list element.
        """
        # Ensure the zero_index is within the bounds of the data array
        zero_index=0
        for ind, element in enumerate(data):
            if isinstance(element, list):
                zero_index=ind
                data[ind] = element[0]

        for element in data:
            if not isinstance(element, (int, float)):
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
            start, stop, step = index
            return [self[idx] for idx in range(start, stop, step)]

        if index >= 0:
            # If the index is non-negative, return from positive_indices if in range
            return self.positive_indices[index] if index < len(self.positive_indices) else 0
        else:
            # If the index is negative, return from negative_indices after flipping sign
            index = -index - 1  # Convert negative index to zero-based positive index for negative_indices
            return self.negative_indices[index] if index < len(self.negative_indices) else 0

    def __setitem__(self, index, value):
        """
        Set the signal value at the specified index.
        """

        if not isinstance(index, int):
            raise TypeError("Indexing only supports integers.")

        if not isinstance(value, (int, float)):
            raise TypeError("DigitalSignal values can only be scalars.")

        if index >= 0:
            # If the index is non-negative
            if index >= len(self.positive_indices):
                # Extend the list with zeros up to the index being set
                self.positive_indices.extend([0] * (index - len(self.positive_indices) + 1))
            self.positive_indices[index] = value
        else:
            # If the index is negative
            index = -index - 1
            if index >= len(self.negative_indices):
                # Extend the list with zeros up to the index being set
                self.negative_indices.extend([0] * (index - len(self.negative_indices) + 1))
            self.negative_indices[index] = value

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
        
        if len(clone.positive_indices) is 0:
            clone.positive_indices.append(0)

        return clone

    def __rshift__(self, amount):
        """
        Return a copy of the signal padded with zeros on the negative side by the given amount for cleaner printing.
        """

        if not isinstance(amount, int):
            raise TypeError("Padding only supports integers.")
        
        clone = DigitalSignal()
        clone.positive_indices = self.positive_indices[:]
        clone.negative_indices = self.negative_indices[:]

        # insert padding
        for _ in range(amount):
            clone.negative_indices.append(0)

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

    def __mul__(self, scalar):
        """
        Return a new DigitalSignal scaled by the given scalar.
        """
        if not isinstance(scalar, (int, float)):
            raise TypeError("The scalar must be an integer or float.")

        # Multiply each element in the positive and negative indices by the scalar
        new_pos = [value * scalar for value in self.positive_indices]
        new_neg = [value * scalar for value in self.negative_indices]

        # Return a new Signal object with the scaled lists
        clone = DigitalSignal()
        clone.positive_indices = new_pos
        clone.negative_indices = new_neg
        return clone

    def __rmul__(self, scalar):
        """
        Support scalar multiplication from the right.
        """
        return self.__mul__(scalar)

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
        return self @ (~other)

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
