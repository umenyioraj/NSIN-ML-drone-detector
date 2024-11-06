import numpy as np
from scipy.interpolate import BSpline
from scipy.interpolate import splrep, splev
import matplotlib.pyplot as plt
 
#### this is avoiding the idea of knots 
# less specific to us but same ideagit

# Sample data
x = np.linspace(0, 10, 10)
y = np.sin(x)

# Find spline representation
tck = splrep(x, y)

# Evaluate spline at new points
xnew = np.linspace(0, 10, 200)
ynew = splev(xnew, tck)

# Plotting
plt.plot(xnew, ynew)
plt.scatter(x, y)
plt.title('Spline Interpolation')
plt.xlabel('x')
plt.ylabel('S(x)')
plt.show()