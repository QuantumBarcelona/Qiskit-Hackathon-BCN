def Xmeasure(circuit, qubit, cbit):
    """
    Measure the qubit in the X-basis
    """
    circuit.h(qubit)
    circuit.measure(qubit, cbit)

    return circuit
