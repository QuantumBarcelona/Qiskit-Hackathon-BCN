# %%
# SECOND CIRCUIT STATEVECTORS# Import standard qiskit modules
from qiskit import QuantumCircuit, QuantumRegister
# For doing exact simulation you can use Statevector (feel free to use something else)
from qiskit.quantum_info import Statevector


# %%
# SECOND CIRCUIT STATEVECTORS

def cutted_statevalues(circ,cq,op):
    # Creation of different cq states circuits:
    qnum = circ.num_qubits
    expVal = []
    for c in ["0","1","+","-","r","l","0","1"]:
        label = "0"*(cq-1) + c + "0"*(qnum-cq)
        stateVector = Statevector.from_label(label)
        expVal.append(stateVector.expectation_value(op))
    return expVal



# %%
from lib.circuits.step1 import *
from qiskit.quantum_info.operators import Operator
X = Operator.from_label("X")
circ = get_circ2()
expVal = cutted_statevalues(circ,0,X)