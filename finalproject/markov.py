""" Markov process example

Written by Lucien Gaitskell 2021
(Wheeler School, Linear Algebra)
"""
import numpy as np
np.set_printoptions(precision=2)


# Transition matrix:
T = np.array(
    [
        [0.1, 0.9, 0],
        [0.4, 0, 0.6],
        [0.5, 0.5, 0]
    ]
)


# Starting state:
x = np.array([0.1, 0.8, 0.1])

print("Start: {}".format(x))

# Iterative calculation:
for i in range(100):
    x = T @ x
    if i > 94:
        print("{:5d}: {}".format(i+1, x))
