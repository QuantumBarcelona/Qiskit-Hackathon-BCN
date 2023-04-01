import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 16}) # enlarge fonts


# Import standard qiskit modules 
from qiskit import QuantumCircuit, QuantumRegister


#For doing exact simulation you can use Statevector (feel free to use something else)
from qiskit.quantum_info import Statevector

#Your code here 

#%%

# loading IBMQ account
from qiskit import IBMQ

# IBMQ.save_account('Token') #you can replace TOKEN with your API token string  (https://quantum-computing.ibm.com/lab/docs/iql/manage/account/ibmq)
IBMQ.load_account()

#%%

from qiskit import QuantumCircuit

circ = QuantumCircuit(5,5)
circ.h((range(4)))
circ.cx(())
circ.draw()
