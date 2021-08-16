#  Author:  anonymous, found on www

import numpy as np
import matplotlib.pyplot as plt

# this plots 50 random (x,y) points between (0,0) and (1,1)
#  each with random radius up to 15 point size 

N = 50

# get and print the x values
x = np.random.rand(N)
print('\nx', x)

# get and print the y values
y = np.random.rand(N)
print('\ny', y)

# calculate and print the sizes of the circles
area = np.pi * (15 * np.random.rand(N))**2 # 0 to 15 point radiuses
print('\narea', area)

# plot the 50 circles
plt.scatter(x, y, s=area, alpha=0.5)
plt.show()