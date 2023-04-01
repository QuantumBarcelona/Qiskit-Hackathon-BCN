def Zmeasure(circuit, qubit, cbit):
    """
    Measure the qubit in the Z-basis
    """
    circuit.measure(qubit, cbit)

    return circuit
