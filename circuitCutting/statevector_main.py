#%%
from lib.circuits.step1 import *
from lib.measures import *
from qiskit.quantum_info import Statevector, Operator
import matplotlib.pyplot as mpl
from lib import *
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
mainCirc = Xmeasure(mainCirc,range(5),range(5))
mainCirc.draw(output="mpl")
# %%
histogram(mainCirc,1000)
# %%
