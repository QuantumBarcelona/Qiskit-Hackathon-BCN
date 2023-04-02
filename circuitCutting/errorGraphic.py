# %%
import matplotlib.pyplot as plt 
import numpy as np
from lib.circuits.step1 import *
from lib.executions import *
from lib.measures import *
from simulation.composed import totalExpectation
from qiskit.quantum_info import Operator, Statevector
from simulation.circuit_1_classical_simulation import run_class_circ1
from simulation.circuit_2_classical_simulation import run_class_circ2
from simulation.composed import recompose

# Classic simulation for entire circuit
def expX_class_full(n): # n = number of shots
    mainCirc = get_mainCirc()
    mainCircuit = Xmeasure(mainCirc, range(5), range(5))
    count = histogram(mainCircuit, n)
    # Use Z since we are "measuring" countings
    Z = Operator.from_label("Z")
    # Compute expectation value:
    expectation = 0
    totalTimes = sum(count.values())
    for key, times in count.items():
        state = Statevector.from_label(key)
        expectation += state.expectation_value(Z ^ Z ^ Z ^ Z ^ Z) * times / totalTimes
  
    expected_X = np.abs(1.0-expectation)

    return expected_X

# Classic simulation for split circuit
def expX_class_split(n,circ_func1,circ_func2):
    expect1 = run_class_circ1(n,circ_func1,makeGraph=False)
    expect2 = run_class_circ2(n,circ_func2,makeGraph=False)
    expectation = recompose(expect1,expect2)
    expected_X = np.abs(1.0-expectation)
    return expected_X

N = list(range(1,100,1))
full_circuit_error = np.ndarray(len(N),dtype=float)
split_circuit_error = np.ndarray(len(N),dtype=float)

full_circuit_error = [expX_class_full(n) for n in N]
split_circuit_error = [expX_class_split(n,get_circ1,get_circ2) for n in N]
split_circuit_error_var = [expX_class_split(n,get_circ1_var,get_circ2_var) for n in N]

print(full_circuit_error)
# print(split_circuit_error)
#%%


fig, ax = plt.subplots(1,2,figsize=(15,15))
fig
ax[0].plot(N,full_circuit_error,label="full circuit")
ax[0].plot(N,split_circuit_error, label="split circuit")

ax[1].plot(N,full_circuit_error,label="full circuit")
ax[1].plot(N,split_circuit_error_var, label="split circuit var")


ax[0].legend(loc=9)
ax[0].set_xlabel("Number of simulations")
ax[0].set_ylabel("Error")
ax[0].set_title("Error v number simulations")

ax[0].set_yscale('log')

ax[1].legend(loc=9)
ax[1].set_xlabel("Number of simulations")
ax[1].set_ylabel("Error")
ax[1].set_title("Error v number simulations")

ax[1].set_yscale('log')

plt.show()

# %%
