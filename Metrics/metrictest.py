from metric3 import m3
from metric1 import m1
lit = [0] * 100

for i in range (0, 100):
    lit[i] = pow(i,2)
    print(lit[i])

for i in range (0, 80):
    print(f"{m3(lit, i, 5)}, {i}, {lit[i]}")
