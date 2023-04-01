# %%
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({"font.size": 16})  # enlarge fonts

import sys

sys.path.append("..")

from lib.circuits.step1 import *

# %%
from lib.measures import from_label

# Import standard qiskit modules
from qiskit import Aer, QuantumCircuit, QuantumRegister, execute

# For doing exact simulation you can use Statevector (feel free to use something else)
from qiskit.quantum_info import Statevector
from qiskit.quantum_info.operators import Operator

# %%
def run_class_circ2(s):
    Z = Operator.from_label("Z")


    backend = Aer.get_backend("qasm_simulator")
    shots = s
    expectedValues = {}

    preQubit = 2

    for c in ["0", "1", "+", "-", "r", "l", "0", "1"]:
        label = "0" * (3 - preQubit - 1) + c + "0" * (preQubit)
        stateVector = Statevector.from_label(label)
        circ = QuantumCircuit(3, 3)
        # Initialize the vector on the simulation to be the statevector
        circ.initialize(stateVector, circ.qubits)
        get_circ2(circ)

        from_label("XXX")(circ)

        job = execute(circ, backend, shots=shots)
        result = job.result()
        counts = result.get_counts(circ)

        expectedValues[c] = np.real(
            sum(
                [
                    Statevector.from_label(outcome).expectation_value(Z ^ Z ^ Z) * count / shots
                    for outcome, count in counts.items()
                ]
            )
        )
    
        plt.figure()
        plt.bar(counts.keys(), counts.values())
        plt.title(f"Initial: |{label}$\\rangle$ ($\langle X\\rangle$ = {expectedValues[c]:.2f})")
        plt.xlabel("Measurement outcome")
        plt.ylabel("Counts")
        plt.show()
    return expectedValues

expectedValues = run_class_circ2(1000)

# %%
