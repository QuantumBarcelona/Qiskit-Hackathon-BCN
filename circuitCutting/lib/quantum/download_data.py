import os

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({"font.size": 16})  # enlarge fonts

import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import json

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
