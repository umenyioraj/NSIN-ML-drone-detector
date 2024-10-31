from scipy import interpolate
import matplotlib.pyplot as plt 
import numpy as np 

x = np.linspace(0,10,200)
y = np.sin(x) + 0.5 *np.cos(2*x) 
noise = np.random.normal(0,0.4,len(x))
y = y + noise 

plt.scatter(x,y)
plt.show()

knot_numbers = 30
x_knots = np.linspace(0, 1, knot_numbers + 2) [1:-1]
quantile_knots = np.quantile(x, x_knots)

t_knots, c_coeffs, degree = interpolate.splrep(x,y,t=quantile_knots, s=3)

spline_evaluator = interpolate.BSpline(t_knots, c_coeffs, degree)
yfit = spline_evaluator(x)

plt.figure(figsize=(8,5))
plt.plot(x,y, '.', color="green", label="Original Data") 
plt.plot(x,yfit, '-', color="red", label='Spline fit')
plt.show()
