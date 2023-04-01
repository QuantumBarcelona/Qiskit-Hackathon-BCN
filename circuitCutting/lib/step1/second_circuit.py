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

circ2 = QuantumCircuit(5, 5)
circ2.h(range(1, 3))
circ2.rx(np.pi / 2, 1)
circ2.rx(np.pi / 2, 3)
circ2.cx(3, 1)
circ2.rx(np.pi / 2, 1)
circ2.cx(2, 3)
circ2.rx(np.pi / 2, 2)
circ2.draw()

