# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 04:42:52 2023

@author: migue
"""

import numpy as np
from scipy.sparse import diags
import matplotlib.pyplot as plt
from qiskit.quantum_info import SparsePauliOp
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, execute
from qiskit.algorithms.optimizers import ADAM, SPSA
from qiskit.circuit import QuantumCircuit, Parameter, ParameterVector
from qiskit.algorithms.time_evolvers.variational import ImaginaryMcLachlanPrinciple
from qiskit.algorithms import TimeEvolutionProblem, VarQITE
from qiskit.circuit import Parameter

K = 100  # strike price
sigma = 0.4  # volatility in %
T = 1
r = 0
Smin = 50
Smax = 150
Nqubits = 4

b = -0.5*(0.5 - r/sigma**2)**2 - r/sigma**2
a = 0.5 - r/sigma**2

#Define range of stock price
dS = 5

x = np.linspace(np.log(Smin), np.log(Smax), 2**Nqubits)
dx = (np.log(Smax)-np.log(Smin))/2**Nqubits

S = np.exp(x)

#Define the Payoff Function

def call_payoff(S, K):
    p = np.zeros(len(S))
    for i in range(len(S)):
        p[i] = max(S[i] - K, 0)
    return p

#Define the underlying strike price
K = 100

#Hamiltoniano
nH = 2**Nqubits
H = np.zeros((nH, nH))
H = [np.ones(nH - 1), -2*np.ones(nH), np.ones(nH - 1)]
offset = [-1, 0, 1]
H = diags(H, offset).toarray()
H[0, 0] = -2*b*dx**2
H[-1, -1] = -2*b*dx**2
H[0, 1] = 0
H[-1, -2] = 0
H = 1/(2*dx**2)*H

# coefs = SparsePauliOp.from_operator(H).coeffs

observable = SparsePauliOp.from_operator(H)

#Ansatz Circuit
def Ansatz(thetas, Nqubits, n = 0):
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
    return result.get_statevector(), circuit
    # return circuit

#Calculate the payoff for the option
payoff = call_payoff(S, K)

# Plot the Payoff Graph
fig = plt.figure()
ax = plt.subplot(211)
ax1 = plt.subplot(212)

ax.spines['bottom'].set_position('zero')
ax.plot(S, payoff, '--', color='g')
plt.xlabel('x')
plt.ylabel('Payoff')
plt.title('Call Option Payoff')


psi0 = np.exp(-a*x)*call_payoff(np.exp(x), K)

psi0 = psi0/np.linalg.norm(psi0)
normpsi0 = np.linalg.norm(psi0)
# sol = Ansatz(thetas=np.zeros(18), Nqubits=4)
# print(sol[0])
# print(sol[1])

def f(thetas):
    return np.linalg.norm(Ansatz(thetas,Nqubits,n = 1)[0] - psi0)

initial_thetas = np.random.rand(18)*2*np.pi
optimizer = SPSA(maxiter = 500)
#optimal_thetas, = optimizer.minimize(fun = f, x0 = initial_thetas)
opt_parameters, par0, par1 = optimizer.optimize(18, f, initial_point = initial_thetas)

chi0 = Ansatz(thetas=opt_parameters, Nqubits = 4, n = 1)[0]
# print(chi0.data)
chi0 = np.array(abs(chi0.data))
Vchi0 = chi0*np.exp(a*np.log(S))*1/sigma**2
ax.plot(S,Vchi0)
#ax.plot(S,payoff/Vchi0)

#-----------------------------------------------
#-----------------------------------------------
#-----------------------------------------------

thetas = ParameterVector("theta", 18)

CIRCUIT = Ansatz(thetas, Nqubits)[1]

init_param_values = opt_parameters
var_principle = ImaginaryMcLachlanPrinciple()
evolution_problem = TimeEvolutionProblem(observable, sigma**2*T)
var_qite = VarQITE(CIRCUIT, init_param_values, var_principle, num_timesteps = 10)
evolution_result = var_qite.evolve(evolution_problem)
thetas_result = evolution_result.parameter_values
xn = evolution_result.times

chiFINAL = Ansatz(thetas = thetas_result[-1,:], Nqubits = 4)[0]
chiFINAL = np.array(abs(chiFINAL.data))
#print(chiFINAL) 
VchiFINAL = chiFINAL*np.exp(a*np.log(S) + 2*b*sigma**2)
ax.plot(S,VchiFINAL)
#ax.plot(S,VchiFINAL/Vchi0)

for i in range(17):
    ax1.plot(xn,thetas_result[:,i])

print('We achieve a great estimation for the payoff function in the initial state. \nHowever, when we try to represent the function in the last state (tau = $\sigma^2$), we find that we encountered some computational issue, which leads to a wrong result, even though the reasoning seems correct.')

plt.show()