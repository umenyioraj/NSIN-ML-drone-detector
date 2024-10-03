from metric1 import m1
from metric2 import m2

def m3(z):
    p = 1; # where p is some constant
    return min(m1(z), p*m2(z))