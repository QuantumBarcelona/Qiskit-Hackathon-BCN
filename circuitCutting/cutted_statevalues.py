# %%
# SECOND CIRCUIT STATEVECTORS# Import standard qiskit modules
from qiskit import QuantumCircuit, QuantumRegister
# For doing exact simulation you can use Statevector (feel free to use something else)
from qiskit.quantum_info import Statevector


# %%
# SECOND CIRCUIT STATEVECTORS

def cutted_statevalues(circ,cq):
    # Creation of different cq states circuits:
    qnum = QuantumCircuit.num_qubits(circ)
    label = "0"*qnum
    expVal = []
    for c in ["0","1","+","-","r","l"]:
        label[cq] = c
        stateVector = Statevector.from_label(label)
        expVal.append(stateVector.expectation_value())
    print(expVal)
    return expVal
# %%
