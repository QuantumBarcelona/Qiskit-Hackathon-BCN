# %%
# Compute the composed expectation from cutted_statevalues
import numpy as np
from circuit_1_classical_simulation import \
    expectedValues as circuit1expectations
from circuit_2_classical_simulation import \
    expectedValues as circuit2expectations

def recompose(circuit1expectations,circuit2expectations):
# Coefficients:
    coefficients = [1 / 2, 1 / 2, 1 / 2, -1 / 2, 1 / 2, -1 / 2, 1 / 2, -1 / 2]
    expectation1 = [circuit1expectations[v] for v in "IIXXYYZZ"]
    expectation2 = [circuit2expectations[v] for v in "01+-rl01"]

    totalExpectation = 0
    for prod in zip(coefficients, expectation1, expectation2):
        totalExpectation += np.prod(prod)
        print(prod)

    print("Final expectation:", totalExpectation)
    return totalExpectation

totalExpectation = recompose(circuit1expectations,circuit2expectations)

# %%
