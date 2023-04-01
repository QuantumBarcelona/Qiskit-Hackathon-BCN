# %%
import matplotlib.pyplot as plt 
import numpy as np
from lib.circuits.step1 import *
from lib.executions import *
from lib.measures import *
from qiskit.quantum_info import Operator, Statevector


def expected_X_full_ciruit(n):
    mainCirc = get_mainCirc()
    mainCircuit = Xmeasure(mainCirc, range(5), range(5))
    count = histogram(mainCircuit, n)

    Z = Operator.from_label("Z")
    # Compute expectation value:
    expectation = 0
    totalTimes = sum(count.values())
    for key, times in count.items():
        state = Statevector.from_label(key)
        expectation += state.expectation_value(Z ^ Z ^ Z ^ Z ^ Z) * times / totalTimes
  
    expected_X_full_ciruit = np.abs(1-expectation)

    return expected_X_full_ciruit

# def expected_X_split_ciruit(n):
    
#     expected_X_split_ciruit = abs(1-expectation)
#     return expected_X_split_ciruit


N = list(range(1,100,1))
full_circuit_error = np.ndarray(len(N),dtype=float)
split_circuit_error = np.ndarray(len(N),dtype=float)

full_circuit_error = [expected_X_full_ciruit(n) for n in N]
# split_circuit_error = [expected_X_split_ciruit(n) for n in N]

print(full_circuit_error)
# print(split_circuit_error)

fig, ax = plt.subplots()
ax.plot(N,full_circuit_error)
# ax.plot(N,split_circuit_error)

ax.set_yscale('log')

plt.show()

# %%
