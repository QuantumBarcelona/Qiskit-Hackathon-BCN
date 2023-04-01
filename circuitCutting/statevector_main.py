#%%
from lib.circuits.step1 import *
from lib.measures import *
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as mpl

# %%0
mainCircuit = get_mainCirc()
mainCirc = Xmeasure(mainCircuit,range(3),range(3))
mainCirc.draw(output="mpl")
# %%