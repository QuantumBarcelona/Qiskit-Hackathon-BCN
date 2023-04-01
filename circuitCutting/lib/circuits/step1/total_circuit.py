# %%
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({"font.size": 16})  # enlarge fonts


# Import standard qiskit modules
from qiskit import QuantumCircuit, QuantumRegister

# For doing exact simulation you can use Statevector (feel free to use something else)
from qiskit.quantum_info import Statevector

# %%
# MAIN CIRCUIT

def get_mainCirc():
    circ = QuantumCircuit(5, 5)
    circ.h(range(5))
    circ.cx(0, 4)
    circ.rx(np.pi / 2, 4)
    circ.cx(0, 3)
    circ.rx(np.pi / 2, 0)
    circ.rx(np.pi / 2, 1)
    circ.rx(np.pi / 5, 3)
    circ.cx(3, 1)
    circ.rx(np.pi / 2, 1)
    circ.cx(2, 3)
    circ.rx(np.pi / 2, 2)
    return circ
# %%
