from metric1 import m1
from metric2 import m2

def m3(z, k_0, T,rate):
    p = 1; # where p is some constant
    return min(m1(z, k_0, T,rate), 0.5*m2(z, k_0, T,rate))