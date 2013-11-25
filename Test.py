import numpy as np
import matplotlib.pyplot as plt
import ExtinctionFunction
a = np.arange(300,1210,10)
b = [ExtinctionFunction.transmission(x, .5, 3.1) for x in a]
plt.plot(a,b)
plt.show()