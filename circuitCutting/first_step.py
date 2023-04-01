# %%
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({"font.size": 16})  # enlarge fonts

from lib.step1 import *

# Import standard qiskit modules
from qiskit import QuantumCircuit, QuantumRegister

# For doing exact simulation you can use Statevector (feel free to use something else)
from qiskit.quantum_info import Statevector

# %%
cricFraction1.draw(output="mpl")
# %%
cricFraction2.draw(output="mpl")
# %%
mainCircuit.draw(output="mpl")

# %%