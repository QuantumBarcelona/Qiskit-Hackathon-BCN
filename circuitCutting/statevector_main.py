#%%
from lib.circuits.step1 import *
from lib.measures import *
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as mpl
#%%
mainCirc = get_mainCirc()
mainCirc.draw(output="mpl")
# Statevector + valor esperat
# Statevector is from whole circuit!
statevector = Statevector.from_instruction(mainCirc)
print(statevector)

# %%
mainCirc = Xmeasure(mainCirc,range(5),range(5))