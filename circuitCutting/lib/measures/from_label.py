from .axis import *

mapping = {
    "I": Imeasure,
    "X": Xmeasure,
    "Y": Ymeasure,
    "Z": Zmeasure,
}


def from_label(label):
    """Returns the measurement functions that must be ran to add measurements to a circuit.

    Parameters
    ----------
    label : str
        The label of the measurement to be performed. (For example, "XIX" or "YIY", which runs the
        measurement of the X operator on the first and third qubits.)
    """

    def measure(circuit):
        for i, char in enumerate(label):
            mapping[char](circuit, i, i)
        return circuit

    return measure
