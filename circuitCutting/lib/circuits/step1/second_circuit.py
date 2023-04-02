# %%
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({"font.size": 16})  # enlarge fonts


# Import standard qiskit modules
from qiskit import QuantumCircuit, QuantumRegister

# For doing exact simulation you can use Statevector (feel free to use something else)
from qiskit.quantum_info import Statevector

# %%
# SECOND PART CIRCUIT


def get_circ2(initialCircuit=None):
    if not initialCircuit:
        circ2 = QuantumCircuit(3, 3)
    else:
        circ2 = initialCircuit
    circ2.h([1, 2])
    circ2.rx(np.pi / 2, 1)
    circ2.rx(np.pi / 5, 0)
    circ2.cx(0, 1)
    circ2.rx(np.pi / 2, 1)
    circ2.cx(2, 0)
    circ2.rx(np.pi / 2, 2)
    return circ2
