import os

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({"font.size": 16})  # enlarge fonts

import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
from concurrent.futures import ThreadPoolExecutor

from lib.circuits.step1 import *
from lib.measures import measure_from_label
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Statevector
from qiskit.quantum_info.operators import Operator
from qiskit_ibm_provider import IBMProvider

provider = IBMProvider(os.environ["IBMQ_TOKEN"])

hub = "ibm-q-community"
group = "digiq-icfo-hack"
project = "main"

backend_name = "ibmq_jakarta"  # 7 qubits
# backend_name = "ibmq_guadalupe	" # 16 qubits

backend = provider.get_backend(backend_name, instance=f"{hub}/{group}/{project}")

Z = Operator.from_label("Z")

shots: int = 1000  # Number of shots to run each circuit for
outFolder = os.path.join(os.path.dirname(__file__), "quantum_out")

pool = ThreadPoolExecutor(max_workers=12)
jobs = {}


def run_simulation(circuit):
    transpiledCirc = transpile(circuit, backend)
    job = backend.run(transpiledCirc, shots=shots, job_tags=["Plan B", "bcn_hackathon"])
    result = job.result()
    counts = result.get_counts(circ)
    return counts


print("QUEUEING JOBS...")


print("Running first circuit...")
for m in ["I", "X", "Y", "Z"]:
    print(f"    Running measurement {m}...")
    circ = get_circ1()
    measure_from_label(f"XX{m}")(circ)

    jobs[m] = pool.submit(run_simulation, circ)


cutQubit = 0
print("Running second circuit...")
for c in ["0", "1", "+", "-", "r", "l"]:
    label = "0" * (3 - cutQubit - 1) + c + "0" * cutQubit
    print(f"    Running circuit with label {label}...")
    stateVector = Statevector.from_label(label)
    circ = QuantumCircuit(3, 3)
    # Initialize the vector on the simulation to be the statevector
    circ.initialize(stateVector, circ.qubits)
    get_circ2(circ)

    measure_from_label("XXX")(circ)

    jobs[c] = pool.submit(run_simulation, circ)


print("Running main circuit...")
circ = get_mainCirc()
measure_from_label("XXXXX")(circ)
jobs["main"] = pool.submit(run_simulation, circ)


print("COLLECTING RESULTS...")


JSON = {}
JSON["first_circuit"] = {}
JSON["second_circuit"] = {}

file = open(os.path.join(outFolder, "first_circuit.txt"), "w")
for m in ["I", "X", "Y", "Z"]:
    print(f"Measurement {m}:")
    counts = jobs[m].result()
    JSON["first_circuit"][m] = {}
    print("    Counts: ", counts)
    JSON["first_circuit"][m]["counts"] = counts

    if m != "I":
        expectedVal = sum(
            [
                np.real(Statevector.from_label(label).expectation_value(Z ^ Z ^ Z)) * count / shots
                for label, count in counts.items()
            ]
        )
    else:
        expectedVal = sum(counts.values()) / shots

    print(f"    Expected value: {expectedVal:.2f}")
    file.write(f"{m}\t{expectedVal}\n")
    JSON["first_circuit"][m]["expected_value"] = expectedVal

    plt.figure()
    plt.bar(counts.keys(), counts.values())
    plt.title(f"Measurement {m} ($\langle {m}\\rangle$ = {expectedVal:.2f})")
    plt.xlabel("Measurement outcome")
    plt.ylabel("Counts")
    plt.savefig(os.path.join(outFolder, f"first_circuit_{m}.png"))
    print("    Saved figure!")

file.close()
with open(os.path.join(outFolder, "quantum.json"), "w") as f:
    json.dump(JSON, f)


file = open(os.path.join(outFolder, "second_circuit.txt"), "w")
for c in ["0", "1", "+", "-", "r", "l"]:
    label = "0" * (3 - cutQubit - 1) + c + "0" * cutQubit
    print(f"Circuit with label {c}:")
    counts = jobs[c].result()
    JSON["second_circuit"][c] = {}
    print("    Counts: ", counts)
    JSON["second_circuit"][c]["counts"] = counts

    expectedVal = np.real(
        sum(
            [
                Statevector.from_label(outcome).expectation_value(Z ^ Z ^ Z) * count / shots
                for outcome, count in counts.items()
            ]
        )
    )
    print(f"    Expected value: {expectedVal:.2f}")

    file.write(f"{label}\t{expectedVal}\n")

    JSON["second_circuit"][c]["expected_value"] = expectedVal

    plt.figure()
    plt.bar(counts.keys(), counts.values())
    plt.title(f"Initial: |{label}$\\rangle$ ($\langle X\\rangle$ = {expectedVal:.2f})")
    plt.xlabel("Measurement outcome")
    plt.ylabel("Counts")
    plt.savefig(os.path.join(outFolder, f"second_circuit_{c}.png"))
    print("    Saved figure!")

file.close()
with open(os.path.join(outFolder, "quantum.json"), "w") as f:
    json.dump(JSON, f)

# Total simulation
JSON["main"] = {}

print("Main circuit:")
print("    Counts: ", counts)
JSON["main"]["counts"] = counts

expectedVal = np.real(
    sum(
        [
            Statevector.from_label(outcome).expectation_value(Z ^ Z ^ Z ^ Z ^ Z) * count / shots
            for outcome, count in counts.items()
        ]
    )
)

print(f"    Expected value: {expectedVal:.2f}")

JSON["main"]["expected_value"] = expectedVal

plt.figure()
plt.bar(counts.keys(), counts.values())
plt.title(f"Initial: |{label}$\\rangle$ ($\langle X\\rangle$ = {expectedVal:.2f})")
plt.xlabel("Measurement outcome")
plt.ylabel("Counts")
plt.savefig(os.path.join(outFolder, f"main_circuit.png"))

print("    Saved figure!")

with open(os.path.join(outFolder, "quantum.json"), "w") as f:
    json.dump(JSON, f)

print("Done!")
