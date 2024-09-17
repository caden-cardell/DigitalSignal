# TODO:
# add error and type checking for signal vs correlation? specifically lag based? 

class DigitalSignal:
    def __init__(self, data=[]):
        """
        Initialize the Signal object.
        
        Args:
        - data (list or array-like): The entire signal array.
        - zero_index (int): The index in 'data' that represents the zero index.
        """
        # Ensure the zero_index is within the bounds of the data array
        zero_index=0
        for ind, element in enumerate(data):
            if isinstance(element, list):
                zero_index=ind
                data[ind] = element[0]

        if len(data) > 0:
            if zero_index < 0 or zero_index >= len(data):
                raise ValueError("zero_index must be within the range of the data array.")
        else:
            if zero_index != 0:
                raise ValueError("zero_index must be within the range of the data array.")
            
        # Separate the data into positive and negative indices
        self.positive_indices = data[zero_index:]    # Values at 0 and positive indices
        self.negative_indices = data[:zero_index][::-1]  # Values at negative indices (reversed order)

    def __getitem__(self, index):
        """
        Overload the indexing operator to access signal values.
        
        Args:
        - index (int): The index to access.

        Returns:
        - The value of the signal at the given index.
        """
        if index >= 0:
            # If the index is non-negative, return from positive_indices if in range
            return self.positive_indices[index] if index < len(self.positive_indices) else 0
        else:
            # If the index is negative, return from negative_indices after flipping sign
            index = -index - 1  # Convert negative index to zero-based positive index for negative_indices
            return self.negative_indices[index] if index < len(self.negative_indices) else 0

    def __setitem__(self, index, value):
        """
        Overload the indexing operator to set signal values.
        
        Args:
        - index (int): The index to set.
        - value: The value to set at the given index.
        """
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
        Shift the zero index by the specified amount on a clone of the signal
        and return the shifted clone.

        Args:
        - amount (int): The number of positions to shift. 
        Negative values shift from negative to positive, 
        and positive values shift from positive to negative.

        Returns:
        - Signal: A new Signal object with the shifted zero index.
        """
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
        
        return clone

    def __add__(self, other):
        """
        Adds two Signal objects together index-wise and returns a new Signal object.
        It keeps the zero index where it is and properly expands the lists 
        to account for the larger size if one has more elements.

        Args:
        - other (Signal): Another Signal object to add.

        Returns:
        - Signal: A new Signal object representing the sum of the two signals.
        """
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
        Subtract one Signal object from another and return a new Signal object.
        
        Args:
        - other (Signal): Another Signal object to subtract.

        Returns:
        - Signal: A new Signal object representing the difference between the two signals.
        """
        if not isinstance(other, DigitalSignal):
            raise TypeError("Subtraction is only supported between two Signal objects.")
        
        # Multiply the 'other' signal by -1 and add it to the current signal
        return self.__add__(other * -1)

    def __mul__(self, scalar):
        """
        Multiply the Signal object by a scalar (float or int) and return a new Signal object.
        
        Args:
        - scalar (float or int): The scalar to multiply the signal by.

        Returns:
        - Signal: A new Signal object where each value is multiplied by the scalar.
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
        Right multiplication to support scalar * Signal.
        This method calls __mul__ to handle the multiplication.
        """
        return self.__mul__(scalar)

    def __neg__(self):
        """
        Unary negation operator for the Signal object.

        This method is called when the unary negation operator (`-`) is applied to an instance of the Signal class. 
        It returns a new Signal object where all the values are negated (multiplied by -1).

        Returns:
        - Signal: A new Signal object that represents the negated version of the original signal.
                  All positive and negative indices are multiplied by -1.
        """
        return -1 * self
    
    def __mod__(self, other):
        return self @ (~other)
    
    def __matmul__(self, other):

        if not isinstance(other, DigitalSignal):
            raise TypeError("Matrix multiplication is only supported between two Signal objects.")

        # Determine the maximum lag value
        len_self = len(self.positive_indices) + len(self.negative_indices)
        len_other = len(other.positive_indices) + len(other.negative_indices)
        len_max = max(len_self, len_other)
    
        n_range = [i for i in range(-(len_max-1), len_max)]
    
        # Initialize a list for storing cross-correlation results
        conv = Signal()

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
    
    def __invert__(self):
        """
        Overload the bitwise NOT (~) operator for the Signal object.
        This method returns a new Signal object where the order of elements is inverted.
        
        Returns:
        - Signal: A new Signal object with the order of elements inverted.
        """
        inverse = DigitalSignal()
        inverse.positive_indices = self.negative_indices[:]
        inverse.positive_indices.insert(0, self.positive_indices[0])
        inverse.negative_indices = self.positive_indices[1:]

        return inverse



    def __len__(self):
        return len(self.negative_indices) + len(self.positive_indices)
    
    def __rshift__(self, amount):
        if not isinstance(amount, int):
            raise TypeError("Padding only supports integers.")
        
        clone = DigitalSignal()
        clone.positive_indices = self.positive_indices[:]
        clone.negative_indices = self.negative_indices[:]

        # insert padding
        for _ in range(amount):
            clone.negative_indices.append(0)

        return clone

    def __repr__(self):
        """
        String representation of the Signal object.
        """
        neg = self.negative_indices[:]
        neg.reverse()
        pos = self.positive_indices[:]
        return f"Signal({' '.join(map(str, neg))} [{pos[0]}] {' '.join(map(str, pos[1:]))})"
