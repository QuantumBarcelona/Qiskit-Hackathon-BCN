#%%
from lib.circuits.step1 import *
from lib.measures import *
from qiskit.quantum_info import Statevector, Operator
import matplotlib.pyplot as mpl
from lib.executions import *
#%%
mainCirc = get_mainCirc()
mainCirc.draw(output="mpl")
# Statevector + valor esperat
# Statevector is from whole circuit!
statevector = Statevector.from_instruction(mainCirc)
print(statevector)

X = Operator.from_label("X")
Result = statevector.expectation_value(X^X^X^X^X)
print(Result)
# %%
mainCircuit = Xmeasure(mainCirc,range(5),range(5))
mainCircuit.draw(output="mpl")
# %%
histogram(mainCircuit,1000)
# %%
