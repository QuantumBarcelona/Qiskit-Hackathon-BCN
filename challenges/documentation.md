# 33 Documentation

## 1.1 Calculate expected values of the Heisenberg Hamiltonian

The Heisenberg Hamiltonian is expressed as follows:

$$ H_{XXZ} = -\frac{1}{4}\sum_{i=1}^N \sigma_i^x\sigma_{i+1}^x + \sigma_i^y\sigma_{i+1}^y + \Delta \, \sigma_i^z\sigma_{i+1}^z $$

Where $\Delta$ describes in which fase we are. To calculate the hamiltonian expected  value, we can use its linearity property to compute each term expected value, so we can define a circuit for each hamiltonian term separately. For instance, for $N=12$ we will have 36 circuits to calculate all the terms expected values, and by summing we finally get the hamiltonian expected value.

$$\langle H_{XXZ}\rangle = -\frac{1}{4}\sum_{i=1}^N \langle\sigma_i^x\sigma_{i+1}^x\rangle + \langle\sigma_i^y\sigma_{i+1}^y\rangle + \Delta \, \langle\sigma_i^z\sigma_{i+1}^z\rangle $$

To calculate the energy of the *Ground State* (from now on *GS*) for $\Delta = 4$, we need the *GS* itself, but knowing that $\Delta = 4$ describes a ferromagnetic fase, we know that the *GS* must be a state with all the spins in the same direction. So we can create a circuit with all the qubits in the $|0 \rangle$ state. Then we can map each term of the hamiltonian to a circuit and let the circuit evolve. Finally with the number of counts in the $|0\rangle^{\otimes N}$ we can calculate the expected value. To do that, we know that $H_k|\psi\rangle = \sum c_i |\xi_i\rangle$ where $|\xi_i\rangle$ are the base vectors (that are orthonormal), $H_k$ is each of the unitary terms, so that $H=\sum_k H_k$. If we apply a $\langle \psi |$ state, we get $\langle \psi |H_k|\psi\rangle = \langle \psi |\sum c_i |\xi_i\rangle$. But to get that, we mesure the probabilities, i.e. $|c|^2_i$. Then, the expected value will be $c_i=\sqrt{\frac{counts}{total\ counts}}$. 

We can express the total expected value:

$$H=-\frac{1}{4}\sum_{i=1}^Nc_i^x+c_i^y+\Delta c_i^z$$

To compute the solution 




### Problems
------------------

1. We didn't know how to plan the first exercise, because of the `HeisenbergModel` methods. We hopped that with that class we could implement it, but we had to really understand what do we had to calculate, so we could split the expected values using the linearity and calculate the expected values for each terms.
2. Because of the first problem, the second problem was harder to develop, because we thought we had to hard-code the hamiltonian, but with this approach we had to compute matrix operations with matrix $2^{12}\times 2^{12}$. Then we realised how to use the `HeisenbergModel` class, so the calculations sped up.
3. When we got to the `VQE`, we didn't import correctly this algorithm, because if you import it from `qiskit.algorithms`, you get the deprecated version. After some research we realised that we had to import it from the `qiskit.algorithms.minimum_eigensolvers`. We created an issue in GitHub that now is closed, as this import has a reason to exist: some ancient code will be broken if this import wasn't like this.
4. Going to the phase diagram, the computation of the expected values was not trivial: we had to compute first a *GS* with the ``VQE`` and then use the `aux_operators`.
5. num particles
6. docs no actualizados
7. tutorial no completo para ir de deprecated a no deprecated
8. tutorials no actualitzats