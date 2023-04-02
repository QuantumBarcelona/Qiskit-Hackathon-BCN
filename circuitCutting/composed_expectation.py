# %%
# Compute the composed expectation from cutted_statevalues
import numpy as np
from cutted_statevalues import expVal as pt2expectedValues
from first_expectations import expected_i, expected_x, expected_y, expected_z

# Coefficients:
coefficients = [1 / 2, 1 / 2, 1 / 2, -1 / 2, 1 / 2, -1 / 2, 1 / 2, -1 / 2]
expectedValues = [expected_i, expected_i, expected_x, expected_x, expected_y, expected_y, expected_z, expected_z]

totalExpectation = 0
for prod in zip(coefficients, expectedValues, pt2expectedValues):
    totalExpectation += np.prod(prod)
    print(prod)

print("Final expectation:", totalExpectation)

# %%
