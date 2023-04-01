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

# %%
# MAIN CIRCUIT

circ = QuantumCircuit(5, 5)
circ.h(range(5))
circ.cx(0, 4)
circ.rx(np.pi / 2, 4)
circ.cx(0, 3)
circ.rx(np.pi / 2, 0)
circ.rx(np.pi / 2, 1)
circ.rx(np.pi / 2, 3)
circ.cx(3, 1)
circ.rx(np.pi / 2, 1)
circ.cx(2, 3)
circ.rx(np.pi / 2, 2)
circ.barrier(range(5))
circ.measure((range(5)), (range(5)))
circ.draw(output="mpl")
