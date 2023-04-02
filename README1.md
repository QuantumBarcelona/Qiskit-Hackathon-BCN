# Qisikit_Hackathon_BCN

## Black-Scholes mode

The Black-Scholes model is a mathematical model used to calculate the theoretical price of European-style options, which are financial derivatives that give the holder the right (but not the obligation) to buy or sell an underlying asset at a predetermined price and time[^1]. The model was developed by Fischer Black and Myron Scholes in the early 1970s[^2] and is widely used in finance to estimate the fair price of options.

The Black-Scholes differential equation is given by:

$$ \frac{∂C}{∂t} + \frac{1}{2} σ^2 S^2 \frac{∂^2C}{∂S^2} + rS \frac{∂C}{∂S} - rC = 0$$

- $C$ is the price of the call option as a function of the underlying asset price $S$ and time $t$.
- $σ$ is the volatility of the underlying asset.
- $r$ is the risk-free interest rate.

The Black-Scholes model is based on several assumptions, including 

1. The underlying asset follows a log-normal distribution.
2. No dividends are paid during the life of the option.
3. No transaction costs or taxes.
4. The risk-free rate and volatility of the underlying asset are constant over the life of the option.
5. The option is European-style.

The formula for the Black-Scholes model takes into account several factors, including the current price of the underlying asset, the exercise price of the option, the time to expiration of the option, the risk-free rate of interest, and the volatility of the underlying asset. By inputting these factors into the formula, the model calculates the theoretical price of the option.

The Black-Scholes model has had a significant impact on the field of finance, and it is widely used by traders, investors, and academics. However, it has also been subject to criticism and limitations, including its assumptions and the fact that it may not accurately predict actual market prices.

## Methodology

To solve the Black-Scholes differential equation, we need to firstly transform the equation into a "Schrödinger equation“, then find the eigenstates corresponding to the Schrödinger Hamiltonian.

Here are the steps of solving the eigenstates in Qiskit:

1. Define your Hamiltonian: You can define your Hamiltonian as a linear combination of Pauli operators using the `WeightedPauliOperator` class in Qiskit.
2. Choose an ansatz: An ansatz is a quantum circuit that is used to prepare a trial wavefunction. You can choose an ansatz from the pre-defined templates in Qiskit, such as the `TwoLocal` ansatz or the `EfficientSU2` ansatz, or you can define your own custom ansatz.
3. Set up the VQE algorithm: You can set up the VQE algorithm using the `VQE` class in Qiskit. You will need to provide the Hamiltonian, the ansatz, and the optimizer to use for minimizing the energy.
4. Run the VQE algorithm: You can run the VQE algorithm using the `run` method of the `VQE` class. This will minimize the energy of the Hamiltonian with respect to the parameters of the ansatz.
5. Extract the eigenstate: Once the VQE algorithm has converged, you can extract the eigenstate of the Hamiltonian by measuring the final state of the quantum circuit. You can do this using the `Statevector` class in Qiskit.

## Mathematical Processing

Reform the Black-Scholes differential equation:

$$  - \frac{1}{2} \hbar σ^2 S^2 \frac{∂^2C}{∂S^2} - \hbar rS \frac{∂C}{∂S} + \hbar rC = i\hbar\frac{∂C}{∂(it)} $$

Since

$$ \frac{∂C}{∂S} = \frac{∂C}{∂\ln S}\frac{∂\ln S}{∂S}=\frac1S\frac{∂C}{∂\ln S}$$

We can change the independent variables into $x =\ln S$, $\tau = it$

$$  (- \frac{1}{2} \hbar \sigma^2 \frac{∂^2}{∂x^2} - \hbar r\frac{∂}{∂x} + \hbar r)C = i\hbar\frac{∂C}{∂\tau} $$

⬆️ wrong

Which is the Schrödinger equation with the Hamiltonian

$$ \hat{H}=- \frac{\hbar^2}{2m} \frac{∂^2}{∂x^2} +r( \frac\hbar\sigma \frac{∂}{∂x} + \hbar ), \quad m=\frac{\hbar}{\sigma}$$

We assume the risk-free interest rate $r$ is small, then the Hamiltonian can be written as

$$ \hat{H} = \hat{H}_0 + r\hat{H}_1$$

where

$$\begin{aligned}\hat{H}_0=&\frac{\hbar^2}{2m} \frac{∂^2}{∂x^2}\\ \hat{H}_1=& \frac\hbar\sigma \frac{∂}{∂x} + \hbar \end{aligned}$$

###  References

[^1]: Hull, J. C. (2018). Options, futures, and other derivatives. Pearson.
[^2]: Black, F., & Scholes, M. (1973). The pricing of options and corporate liabilities. Journal of Political Economy, 81(3), 637-654.

