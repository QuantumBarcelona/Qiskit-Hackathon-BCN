# %%
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({"font.size": 16})  # enlarge fonts

import sys

sys.path.append("..")

from lib.circuits.step1 import *

# Import standard qiskit modules
from qiskit import Aer, QuantumCircuit, QuantumRegister, execute

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
# This initializes the statevector at the |0> state (all zeros), and then evolves it under the circuit
stateVector = Statevector.from_instruction(get_circ1())

print("Expected value of X:", stateVector.expectation_value(X ^ X ^ X))
print("Expected value of Y:", stateVector.expectation_value(X ^ Y ^ X))
print("Expected value of Z:", stateVector.expectation_value(X ^ Z ^ X))
print("Expected value of I:", stateVector.expectation_value(X ^ I ^ X))

# %%
from lib.measures import from_label

backend = Aer.get_backend("qasm_simulator")
shots = 1000
expectedValues = {
    "I": 0,
    "X": 0,
    "Y": 0,
    "Z": 0,
}

for m in expectedValues.keys():
    circ = get_circ1()
    from_label(f"X{m}X")(circ)

    job = execute(circ, backend, shots=shots)
    result = job.result()
    counts = result.get_counts(circ)

    if m != "I":
        expectedValues[m] = sum(
            [
                np.real(Statevector.from_label(label).expectation_value(Z ^ Z ^ Z)) * count / shots
                for label, count in counts.items()
            ]
        )
    else:
        expectedValues[m] = sum(counts.values()) / shots

    plt.figure()
    plt.bar(counts.keys(), counts.values())
    plt.title(f"Measurement {m} ($\langle {m}\\rangle$ = {expectedValues[m]:.2f})")
    plt.xlabel("Measurement outcome")
    plt.ylabel("Counts")
    plt.show()


# %%
