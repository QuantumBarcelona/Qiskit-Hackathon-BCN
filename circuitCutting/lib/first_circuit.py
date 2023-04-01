# %%
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({"font.size": 16})  # enlarge fonts


# Import standard qiskit modules
from qiskit import QuantumCircuit, QuantumRegister

# For doing exact simulation you can use Statevector (feel free to use something else)
from qiskit.quantum_info import Statevector

# %%
# First chunk of circuit cutting
"""
q0 --> 0
q3 --> 1
q4 --> 2
"""
#
circ1 = QuantumCircuit(3, 3)
circ1.h([0, 1, 2])  # Hadamard gate
circ1.cx(0, 2)  # Ctrl C gate (target, where applies gate)
circ1.rx(np.pi / 2, 2)  # Rx gate
circ1.cx(0, 1)
circ1.rx(np.pi / 2, 0)
circ1.x([0, 1, 2])
circ1.measure((0, 2), (0, 2))  # Map
circ1.measure(1, 1)  # To change for cutting
circ1.draw(output="mpl")
