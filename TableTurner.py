import numpy as np

a = np.loadtxt("interp_4437.0_-0.5_4.73_0.5.txt")
np.savetxt("interp_4437.0_-0.5_4.73_0.5.txt", np.transpose(a))