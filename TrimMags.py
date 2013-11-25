import numpy as np
import numpy.random as random

mags = np.loadtxt("Mags_g.txt")
out = open("Mags_g_trimmed.txt" , 'w')

print >> out, "# Gaia_G_Mag LSST_U_Mag LSST_G_Mag LSST_R_Mag LSST_I_Mag LSST_Z_Mag LSST_Y4_Mag Temperature Gravity Metallicity a0"
for star in mags:
    if(random.rand() > 0.33):
        print >> out, star[0], star[1], star[2], star[3], star[4], star[5], star[6], star[7], star[8], star[9], star[10]