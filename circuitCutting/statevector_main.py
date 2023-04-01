#%%
import matplotlib.pyplot as mpl
from lib.circuits.step1 import *
from lib.executions import *
from lib.measures import *
from qiskit.quantum_info import Operator, Statevector

#%%
mainCirc = get_mainCirc()
mainCirc.draw(output="mpl")
# Statevector + valor esperat
# Statevector is from whole circuit!
statevector = Statevector.from_instruction(mainCirc)
print(statevector)

X = Operator.from_label("X")
print("X:", X)
Result = statevector.expectation_value(X ^ X ^ X ^ X ^ X)
print(Result)
# %%
mainCircuit = Xmeasure(mainCirc, range(5), range(5))
mainCircuit.draw(output="mpl")
# %%
count = histogram(mainCircuit, 1000)

# %%
Z = Operator.from_label("Z")
# Compute expectation value:
expectation = 0
totalTimes = sum(count.values())
for key, times in count.items():
    state = Statevector.from_label(key)
    expectation += state.expectation_value(Z ^ Z ^ Z ^ Z ^ Z) * times / totalTimes

print("Expectation value:", expectation)
