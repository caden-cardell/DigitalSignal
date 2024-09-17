# Installation Guide
Follow these steps to set up and install the package:

### 1. **Create a new directory**:
```bash
mkdir my_project
cd my_project
```

### 2. **Create a virtual environment**:
```bash
python3 -m venv venv
```

### 3. **Activate the virtual environment**:
On macOS and Linux:
```bash
source venv/bin/activate
```
On Windows:
```bash
venv\Scripts\activate
```

### 4. **Install the package**:
```bash
pip install git+https://github.com/caden-cardell/DigitalSignal.git@latest
```

# Examples

### Autocorrelation
```python
import DigitalSignal

x = DigitalSignal([1, 1, 1, -1, 1])  # Barker Code 5
print(x)  # DigitalSignal([1] 1 1 -1 1)
# the inner bracket around 1 (i.e. [1]) denotes the zero index

r_xx = x % x  # the autocorrelation of x

print(r_xx)  # DigitalSignal(1 0 1 0 [5] 0 1 0 1)
# the inner bracket around 5 (i.e. [5]) denotes the zero index
```

### Timeshifting
```python
import DigitalSignal

x = DigitalSignal([1, 1, 1, -1, 1])  # Barker Code 5
print(x)  # DigitalSignal([1] 1 1 -1 1)

y = x(-1)
print(y)  # DigitalSignal([0] 1 1 1 -1 1)
```

### Negation
```python
import DigitalSignal

x = DigitalSignal([1, 1, 1, -1, 1])  # Barker Code 5
print(x)  # DigitalSignal([1] 1 1 -1 1)

y = -x
print(y)  # DigitalSignal([-1] -1 -1 1 -1)
```

### Scalar multiplication
```python
import DigitalSignal

x = DigitalSignal([1, 1, 1, -1, 1])  # Barker Code 5
print(x)  # DigitalSignal([1] 1 1 -1 1)

y = 2*x
print(y)  # DigitalSignal([2] 2 2 -2 2)
```

### Addition about the zero index
```python
import DigitalSignal

x1 = DigitalSignal([-2, -1, [0]]) 
print(x1)  # DigitalSignal(-2 -1 [0])

x2 = DigitalSignal([[0], 1, 2]) 

y = x1 + x2
print(y)  # DigitalSignal(-2 -1 [0] 1 2)
```

### Reverse about zero index
```python
import DigitalSignal

x = DigitalSignal([-2, -1, [0], 1, 2, 3, 4, 5])
print(x)  # DigitalSignal(-2 -1 [0] 1 2 3 4 5)

y = ~x
print(y)  # DigitalSignal(5 4 3 2 1 [0] -1 -2)
```

### Combination
```python
import DigitalSignal

x = Signal([1, 1, -1])  # Barker Code 3
print(x)  # DigitalSignal([1] 1 -1)

y = 2*x - x(-4)
print(y)  # DigitalSignal([2] 2 -2 0 -1 -1 1)
```

### Convolution
```python
import DigitalSignal

x = DigitalSignal([0, 1, 2, 3])  
print(x)  # DigitalSignal([0] 1 2 3)

h = DigitalSignal([1, 1])
print(x)  # DigitalSignal([1] 1)

y = x @ h  # the convoluation of x with h
print(y)
```