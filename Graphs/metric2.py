from metric1 import m1, q
import math



def c(z, k_0, T, rate):
    c = 0
    for k in range(k_0, k_0+ T - 1):
        c += abs(z[(k+1)*rate] - z[k*rate])

    return c/T

def m2(z, k_0, T, rate):
    return m1(z, k_0, T, rate)/c(z, k_0, T, rate)
