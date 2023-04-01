# %%
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({"font.size": 16})  # enlarge fonts

from lib.histogram import histogram
from lib.measures import Xmeasure, Ymeasure
from lib.step1 import *

# Import standard qiskit modules
from qiskit import QuantumCircuit, QuantumRegister, execute

# For doing exact simulation you can use Statevector (feel free to use something else)
from qiskit.quantum_info import Statevector

# %%
get_mainCirc().draw(output="mpl")
# %%
get_circ1().draw(output="mpl")
# %%
get_circ2().draw(output="mpl")

# %%
# Create the first circuit
circFraction1 = get_circ1()
print(Statevector.from_instruction(circFraction1))

Xmeasure(circFraction1)
Ymeasure(circFraction1)
