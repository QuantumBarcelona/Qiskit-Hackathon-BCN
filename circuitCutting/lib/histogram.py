# %%

from qiskit import QuantumCircuit, Aer, execute
from qiskit.tools.visualization import plot_histogram


# %%
# SIMULATOR WITH HISTOGRAM

def histogram(circ, s):
    backend = Aer.get_backend("qasm_simulator")
    job = execute(circ, backend, shots=s)
    result = job.result()
    counts = result.get_counts(circ)
    return plot_histogram(counts)