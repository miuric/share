from functools import reduce

import numpy as np

a = np.arange(10, 101, 10)


def add(x, y):
    return x + y


print(reduce(add, a))

# 10 -100

# 200 290


a = 10
total = 0
for i in range(15):
    b = np.arange(a, a + 10 * 10, 10)
    print(b)
    total += reduce(add, b)
    a += 10
print(total)

