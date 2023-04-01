import matplotlib.pyplot as plt
from qiskit.circuit.library import TwoLocal
from qiskit import QuantumCircuit
from qiskit.visualization import circuit_drawer

# Define the number of qubits and the type of rotations you want to use
num_qubits = 12
rotation_blocks = ['ry', 'rx']
entanglement_blocks = 'cz'
entanglement = 'circular'

# Define the number of layers for the ansatz
num_layers = 3

# Create the TwoLocal ansatz circuit
ansatz = TwoLocal(
    num_qubits,
    rotation_blocks=rotation_blocks,
    entanglement_blocks=entanglement_blocks,
    entanglement=entanglement,
    reps=num_layers,
    insert_barriers=True
)

print(ansatz)
