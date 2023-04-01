def Ymeasure(circuit, qubit, cbit):
    circuit.sdg(qubit)
    circuit.h(qubit)
    circuit.measure(qubit, cbit)

    circuit.h(qubit)
    circuit.s(qubit)
    return circuit
