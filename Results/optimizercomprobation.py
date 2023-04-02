# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 18:50:19 2023

@author: migue
"""

## Black scholes, simulation parameters and basic imports
from scipy.sparse import diags
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, execute
import matplotlib.pyplot as plt
import numpy as np
from qiskit.algorithms import VQE
from qiskit.circuit.library import EfficientSU2
from qiskit.opflow import PauliSumOp
from qiskit.quantum_info import SparsePauliOp, Pauli
from qiskit.circuit import Parameter
from qiskit.algorithms.optimizers import ADAM, SPSA

##################################################
##################################################
niter = 1000
##################################################
##################################################

K = 100 # strike price
sigma = 0.4 # volatility in %
T = 1
r = 0
Smin = 50
Smax = 150
Nqubits = 4

b = -0.5*(0.5 - r/sigma**2)**2 - r/sigma**2
a = 0.5 - r/sigma**2

#Define range of stock price
dS = 5
dx = dS
S = np.linspace(Smin,Smax,2**Nqubits)
nS = len(S)

#Define the Payoff Function
def call_payoff(S,K):
    p = np.zeros(len(S))
    for i in range(len(S)): p[i] = max(S[i] - K,0)
    return p

#Define the underlying strike price
K = 100

#Hamiltoniano
nH = 2**Nqubits
H = np.zeros((nH,nH))
H = [np.ones(nH - 1),-2*np.ones(nH),np.ones(nH - 1)]
offset = [-1,0,1]
H = diags(H,offset).toarray()
H[0,0] = -2*b*dx**2
H[-1,-1] = -2*b*dx**2
H[0,1] = 0
H[-1,-2] = 0
H = 1/(2*dx**2)*H
#print(H)

coefs = SparsePauliOp.from_operator(H).coeffs #Devuelve la descomposicion de H en matrices de Pauli

pauli_decomp = SparsePauliOp.from_operator(H)

#Ansatz Circuit
def Ansatz(thetas,Nqubits):
    qreg_q = QuantumRegister(Nqubits, 'q')
    creg_c = ClassicalRegister(Nqubits, 'c')
    circuit = QuantumCircuit(qreg_q, creg_c)
        
    circuit.x(qreg_q[0])
    circuit.h(qreg_q[1])
    circuit.h(qreg_q[2])
    circuit.h(qreg_q[3])
    circuit.ry(thetas[0], qreg_q[0])
    circuit.ry(thetas[1], qreg_q[1])
    circuit.ry(thetas[2], qreg_q[2])
    circuit.ry(thetas[3], qreg_q[3])
    circuit.cry(thetas[4], qreg_q[0], qreg_q[1])
    circuit.cry(thetas[5], qreg_q[1], qreg_q[2])
    circuit.ry(thetas[6], qreg_q[0])
    circuit.cry(thetas[7], qreg_q[2], qreg_q[3])
    circuit.ry(thetas[8], qreg_q[1])
    circuit.ry(thetas[9], qreg_q[2])
    circuit.ry(thetas[10], qreg_q[3])
    circuit.cry(thetas[11], qreg_q[0], qreg_q[1])
    circuit.cry(thetas[12], qreg_q[1], qreg_q[2])
    circuit.ry(thetas[13], qreg_q[0])
    circuit.cry(thetas[14], qreg_q[2], qreg_q[3])
    circuit.ry(thetas[15], qreg_q[1])
    circuit.ry(thetas[16], qreg_q[2])
    circuit.ry(thetas[17], qreg_q[3])
    
    backend = Aer.get_backend('statevector_simulator')
    result = execute(circuit, backend).result()
    return result.get_statevector()
    # return circuit

#Calculate the payoff for the option
payoff = call_payoff(S,K) 

x = np.log(S)
psi0 = np.exp(-a*x)*call_payoff(S,K)
psi0 = psi0/np.linalg.norm(psi0)

#OPTIMIZATION
def f(thetas):
    return np.linalg.norm(Ansatz(thetas,Nqubits) - psi0)

initial_thetas = np.random.rand(18)*2*np.pi
optimizer = SPSA(maxiter = niter)
#optimal_thetas, = optimizer.minimize(fun = f, x0 = initial_thetas)
result,par0,par1 = optimizer.optimize(18, f, initial_point = initial_thetas)

PSI0 = Ansatz(result,Nqubits)
PSI0 = np.array(abs(PSI0.data))
print('-----------------------------------------------------------------')
print('MEASURED STATEVECTOR (using parameters computed by the optimizer')
print('-----------------------------------------------------------------')
print(PSI0)
print('-----------------------------------------------------------------')
print('-----------------------------------------------------------------')
print('THEORETICAL STATEVECTOR')
print('-----------------------------------------------------------------')
print(psi0)
print('-----------------------------------------------------------------')
