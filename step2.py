## PUT CODE HERE
import matplotlib.pylab as plt
from qiskit.visualization import plot_histogram
from qiskit import Aer, transpile
from step1 import ansatz
from step1 import get_init_params
import numpy as np


def counts_to_distr(counts):
    """
    Convert Qiskit result counts to dict with integers as
    keys, and pseudo-probabilities as values.
    """
    n_shots = sum(counts.values())
    return {int(k, 2): v/n_shots for k, v in counts.items()}

def create_target_distr(n_qbits, cross_over):
    """
    cross_over is the last zero point
    """
    n_states = 2**n_qbits
    if cross_over >= n_states:
        raise Exception("open your eyes mate")
    end = n_states-cross_over-1
    #print(end)
    cumulant = sum(np.linspace(1, end, end)**2)
    #print(np.linspace(1, end, end)**2)
    target_distr = {}
    for i in range(n_states):
        if i < cross_over:
            target_distr[i] = 0
        else:
            target_distr[i] = (i - cross_over)**2 / cumulant
    return target_distr 


def counts_to_distr(counts):
    """
    Convert Qiskit result counts to dict with integers as
    keys, and probabilities as values.
    """
    n_shots = sum(counts.values())
    probs = {int(k, 2): v/n_shots for k, v in counts.items()}
    
    return probs

def get_sorted_amplitudes(probs):
    """
    Convert Qiskit result counts to dict with integers as
    keys, and pseudo-probabilities as sorted values.
    """
    sorted_amplitudes = {key: np.sqrt(probs[key]) for key in sorted(probs)}
    return sorted_amplitudes

def counts_to_amp(counts):
    """
    Convert Qiskit result counts to dict with integers as
    keys, and pseudo-probabilities as values.
    """
    sq_dict = {key: np.sqrt(value) for key, value in counts.items()}
    n_shots2 = sum(sq_dict.values())
    return {int(k, 2): np.sqrt(v)/n_shots2 for k, v in counts.items()}