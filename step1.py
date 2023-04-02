import numpy as np
from scipy.stats import norm 
from qiskit import QuantumCircuit
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.circuit.library import RealAmplitudes
from qiskit.quantum_info import SparsePauliOp
from qiskit.opflow import PauliSumOp

def black_scholes_european_call_payoff(S0, K, T, r, sigma):
    '''
    Gives the option premium according to the Black-Scholes formula
    
    INPUTS: 
     
    S0 = initial stock price
    K = strike price
    T = option maturity 
    r = annual free-risk interest rate 
    sigma = annual stock volatility
     
    OUTPUTS: 
    
    Option payoffs for European Calls
    '''

    d1 = (np.log(S0/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    return S0 * norm.cdf(d1) - K * np.exp(-r*T)*norm.cdf(d2)

def get_init_params(n_qubits, rep):
    '''Note that initial angles are set to pi/2'''
    params = np.zeros(n_qubits + rep*(2*n_qubits-1))
    for i in range(n_qubits):
        params[i] = np.pi/2
    return params

# define the variational ansatz
def ansatz(params, n_qubits, rep):
    """
        params are the trainable parameters
        n_qubits is the number of qubits in the ansatz
        rep is the repetation of the controlled-RY group
    """
    # giving exceptions
    if len(params) != n_qubits + rep*(2*n_qubits-1):
        raise Exception("the number of parameters doesn't match")
    if n_qubits < 2:
        raise Exception("not enought qubits to build the ansatz")
    if rep < 1:
        raise Exception("the repetation must be at least 1")
    if type(n_qubits) != int:
        raise Exception("the number of qubits must be an integar")
    if type(rep) != int:
        raise Exception("the number of repetation must be an integer")
    
    # build the circuit
    qc = QuantumCircuit(n_qubits)
    qc.x(0)
    qc.h(range(1,n_qubits))
    for n in range(n_qubits):
        qc.ry(params[n], n)
    
    for i in range(rep):
        for n in range(n_qubits-1):
            qc.cry(params[n_qubits+(2*n_qubits-1)*i+n], n, n+1)
            qc.ry(params[n_qubits+(2*n_qubits-1)*i+n+n_qubits-1], n)
        qc.ry(params[n_qubits+(2*n_qubits-1)*i+(2*n_qubits-2)], n_qubits-1)
    return qc


def hamiltonian(qubit_count, delta, r, sigma):

    dim = 2**qubit_count

    b = -1/2 * (1/2-r/sigma**2)**2-r/sigma**2
   
    H = np.zeros((dim, dim))

    H[0][0] = -b*(2*delta**2)

    H[-1][-1] = -b*(2*delta**2)

    for i in range(1, dim-1):
    
        H[i][i-1] = 1

        H[i][i] = -2

        H[i][i+1] = 1

    return H*(1/(2*delta**2))

