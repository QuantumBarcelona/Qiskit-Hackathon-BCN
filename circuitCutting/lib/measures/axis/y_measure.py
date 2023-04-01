def Ymeasure(circuit, qubit, cbit):
    circuit.sdg(qubit)
    circuit.h(qubit)
    circuit.measure(qubit, cbit)

    return circuit
