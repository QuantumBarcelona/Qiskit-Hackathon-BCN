# %%
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({"font.size": 16})  # enlarge fonts

from lib.circuits.step1 import *

# Import standard qiskit modules
from qiskit import QuantumCircuit, QuantumRegister, execute

# For doing exact simulation you can use Statevector (feel free to use something else)
from qiskit.quantum_info import Statevector
from qiskit.quantum_info.operators import Operator

#  %%
# Matrix operators
X = Operator.from_label("X")
Y = Operator.from_label("Y")
Z = Operator.from_label("Z")
I = Operator.from_label("I")

# %%
get_mainCirc().draw(output="mpl")
# %%
get_circ1().draw(output="mpl")
# %%
get_circ2().draw(output="mpl")

# %%

# This initializes the statevector at the |0> state (all zeros), and then evolves it under the circuit
stateVector = Statevector.from_instruction(get_circ1())
print("State vector after the circuit:", stateVector)

# Measureme X everywhere
expected_x = stateVector.expectation_value(X ^ X ^ X)
expected_y = stateVector.expectation_value(X ^ Y ^ X)
expected_z = stateVector.expectation_value(X ^ Z ^ X)
expected_i = stateVector.expectation_value(X ^ I ^ X)

print("Expected value of X:", expected_x)
print("Expected value of Y:", expected_y)
print("Expected value of Z:", expected_z)
print("Expected value of I:", expected_i)

# %%
