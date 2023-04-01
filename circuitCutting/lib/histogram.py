# %%

from qiskit import QuantumCircuit, Aer, execute
from qiskit.tools.visualization import plot_histogram


# %%
# SIMULATOR WITH HISTOGRAM

def histogram(circ):
    backend = Aer.get_backend("qasm_simulator")
    job = execute(circ, backend, shots=10000)
    result = job.result()
    counts = result.get_counts(circ)
    plot_histogram(counts)