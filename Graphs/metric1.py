import math

# list z = 

# z is list of detection variable
# k_0 is the starting index of the frame we want to analyze
# T is the number of seconds over which we sample
# by adding k_0 and T we find the end index of our frame

def q(z, k_0, T):
    q = 0

    for k in range (k_0, k_0 + T - 1):
        q += z[k + 1] - z[k]

    return q/T
    



def m1(z, k_0, T):
    m1 = 0

    for k in range (k_0, k_0 + T - 1):
        m1 += pow(z[k+1] - z[k] - q(z, k_0, T), 2)

    return m1/T