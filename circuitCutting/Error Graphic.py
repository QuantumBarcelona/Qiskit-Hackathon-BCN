# %%
import matplotlib.pyplot as plt 
import numpy as np

def expected_X_full_ciruit(n):
    expected_X_full_ciruit = n**2
    return expected_X_full_ciruit

def expected_X_split_ciruit(n):
    expected_X_split_ciruit = n**3
    return expected_X_split_ciruit


N = list(range(100,1000,100))
full_circuit_error = np.ndarray(len(N),dtype=float)
split_circuit_error = np.ndarray(len(N),dtype=float)

full_circuit_error = [expected_X_full_ciruit(n) for n in N]
split_circuit_error = [expected_X_split_ciruit(n) for n in N]

print(full_circuit_error)
print(split_circuit_error)

fig, ax = plt.subplots()
ax.plot(N,full_circuit_error)
ax.plot(N,split_circuit_error)

ax.set_yscale('log')
ax.set_xscale('log')

plt.show()

# %%
