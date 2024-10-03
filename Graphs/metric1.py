import math

# list z = 

#input z is list of detection variable
def q(z):
    T = 20 #Time horizon in seconds
    k_0 = 0
    q = 0

    for k in range (k_0, k_0 + T - 1):
        q += z[k + 1] - z[k]

    return q/T
    



def m1(z):
    T = 20 #Time horizon in seconds
    k_0 = 0
    m1 = 0
    z = list(range(1,100))

    for k in range (k_0, k_0 + T - 1):
        m1 += pow(z[k+1] - z[k] - q, 2)


    return m1/T