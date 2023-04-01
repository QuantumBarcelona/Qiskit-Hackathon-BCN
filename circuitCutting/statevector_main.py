#%%
from lib.step1 import *
from lib.measures import *
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as mpl

# %%
mainCircuit = Xmeasure(mainCircuit,range(3),range(3))
mainCircuit.draw(output="mpl")
# %%