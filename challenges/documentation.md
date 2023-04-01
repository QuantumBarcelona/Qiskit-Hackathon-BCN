# 33 Documentation

## 1.1 Calculate expected values of the Heisenberg Hamiltonian

The Heisenberg Hamiltonian is expressed as follows:

$$ H_{XXZ} = -\frac{1}{4}\sum_{i=1}^N \sigma_i^x\sigma_{i+1}^x + \sigma_i^y\sigma_{i+1}^y + \Delta \, \sigma_i^z\sigma_{i+1}^z $$

Where $\Delta$ describes in which fase are we. To calculate the expected  value, we can use the linearity property to compute each expected value, so we can define a circuit for each expected value. For instance, for $N=12$ we will have 36 circuits to calculate all the expected values.

$$\langle H_{XXZ}\rangle = -\frac{1}{4}\sum_{i=1}^N \langle\sigma_i^x\sigma_{i+1}^x\rangle + \langle\sigma_i^y\sigma_{i+1}^y\rangle + \Delta \, \langle\sigma_i^z\sigma_{i+1}^z\rangle $$

To calculate the energy of the *Ground State* (from now on *GS*) for $\Delta = 4$, we need the *GS* itself, but knowing that $\Delta = 4$ describes a ferromagnetic fase, we know that the *GS* must be a state with all the spins in the same direction. So we can create a circuit with all the qubits in the $|0 \rangle$ state. Then we can map each term of the hamiltonian to a circuit and let the circuit evolve. Finally with the number of counts in the $|0\rangle^{\otimes N}$ we can calculate the expected value.


### Problems
------------------

1. We didn't know how to plan the first exercise, because of the `HeisenbergModel` methods. We hopped that with that class we could implement it, but we had to really understand what do we had to calculate, so we could split the expected values using the linearity and calculate the expected values for each terms.