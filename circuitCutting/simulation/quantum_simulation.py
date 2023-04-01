import os

import matplotlib.pyplot as plt
import numpy as np
from lib.measures import from_label

plt.rcParams.update({"font.size": 16})  # enlarge fonts

import sys

sys.path.append("..")

from lib.circuits.step1 import *

# Import standard qiskit modules
from qiskit import IBMQ, Aer, QuantumCircuit, QuantumRegister, execute, transpile

# For doing exact simulation you can use Statevector (feel free to use something else)
from qiskit.quantum_info import Statevector
from qiskit.quantum_info.operators import Operator
from qiskit_ibm_provider import IBMProvider

# loading IBMQ account


provider = IBMProvider()

hub = "ibm-q-community"
group = "digiq-icfo-hack"
project = "main"

backend_name = "ibmq_jakarta"  # 7 qubits
# backend_name = "ibmq_guadalupe	" # 16 qubits

backend = provider.get_backend(backend_name, instance=f"{hub}/{group}/{project}")

Z = Operator.from_label("Z")

shots: int = 1024  # Number of shots to run each circuit for
outFolder = os.path.join(os.path.dirname(__file__), "quantum_out")


file = open(os.path.join(outFolder, "first_circuit.txt"), "w")

for m in ["I", "X", "Y", "Z"]:
    circ = get_circ1()
    from_label(f"X{m}X")(circ)

    transpiledCirc = transpile(circ, backend)
    job = backend.run(transpiledCirc, shots=shots, job_tags=["Plan B - first", "bcn_hackathon"])
    result = job.result()
    counts = result.get_counts(circ)

    if m != "I":
        expectedVal = sum(
            [
                np.real(Statevector.from_label(label).expectation_value(Z ^ Z ^ Z)) * count / shots
                for label, count in counts.items()
            ]
        )
    else:
        expectedVal = sum(counts.values()) / shots

    file.write(f"{m}\t{expectedVal}\n")

    plt.figure()
    plt.bar(counts.keys(), counts.values())
    plt.title(f"Measurement {m} ($\langle {m}\\rangle$ = {expectedVal:.2f})")
    plt.xlabel("Measurement outcome")
    plt.ylabel("Counts")
    plt.savefig(os.path.join(outFolder, f"first_circuit_{m}.png"))

file.close()

preQubit = 2
file = open(os.path.join(outFolder, "second_circuit.txt"), "w")

for c in ["0", "1", "+", "-", "r", "l"]:
    label = "0" * (3 - preQubit - 1) + c + "0" * (preQubit)
    stateVector = Statevector.from_label(label)
    circ = QuantumCircuit(3, 3)
    # Initialize the vector on the simulation to be the statevector
    circ.initialize(stateVector, circ.qubits)
    get_circ2(circ)

    from_label("XXX")(circ)

    transpiledCirc = transpile(circ, backend)
    job = backend.run(transpiledCirc, shots=shots, job_tags=["Plan B - second", "bcn_hackathon"])
    result = job.result()
    counts = result.get_counts(circ)

    expectedVal = np.real(
        sum(
            [
                Statevector.from_label(outcome).expectation_value(Z ^ Z ^ Z) * count / shots
                for outcome, count in counts.items()
            ]
        )
    )

    plt.figure()
    plt.bar(counts.keys(), counts.values())
    plt.title(f"Initial: |{label}$\\rangle$ ($\langle X\\rangle$ = {expectedVal:.2f})")
    plt.xlabel("Measurement outcome")
    plt.ylabel("Counts")
    plt.savefig(os.path.join(outFolder, f"second_circuit_{c}.png"))

file.close()
