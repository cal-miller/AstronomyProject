import numpy as np
import scipy as sp
import scipy.stats as stat
from scipy import interpolate
def InterpolateMagnitudes(data, temp_grid, metallicity_grid, gravity_grid):
    eval_grid = np.meshgrid(temp_grid, gravity_grid, metallicity_grid)
    eval_points = np.empty((len(np.ravel(eval_grid[0])),3))
    eval_points[:,0], eval_points[:,1], eval_points[:,2] = np.ravel(eval_grid[0]), np.ravel(eval_grid[1]), np.ravel(eval_grid[2])
    points = np.empty((len(data[:,1]),3))
    points[:,0], points[:,1], points[:,2] = data[:,7], data[:,8], data[:,9]
    mags = np.empty((len(eval_points[:,0]),6))
    for band in range(1,7):
        values = data[:,band]
        mags[:,band-1] = interpolate.griddata(points, values, eval_points)
    temperature, gravity, metallicity = eval_points[:,0], eval_points[:,1], eval_points[:,2]
    return(mags, temperature, gravity, metallicity)

np.set_printoptions(threshold=np.nan)
file = np.loadtxt('Mags_g.txt')
pointsDict = {"T":0, "G":1, "Z":2}
mags, temperature, gravity, metallicity = InterpolateMagnitudes(file, np.arange(4400,8500,20), np.arange(-2,0,.05), np.arange(4.4,4.75,.05))
output = np.empty((len(temperature),9))
output[:,0:6], output[:,6], output[:,7], output[:,8] = mags[:,0:6], temperature, gravity, metallicity
np.savetxt('interp_mags.txt', output, header = 'LSST_U_Mag LSST_G_Mag LSST_R_Mag LSST_I_Mag LSST_Z_Mag LSST_Y4_Mag Temperature Gravity Metallicity')
points_file = np.loadtxt('SamplePoints.txt')
stats_file = open("InterpStats.txt" , 'w')
for count in range(0,len(points_file[:,0])):
    temp = points_file[count,0]
    z = points_file[count,2]
    g = points_file[count,1]
    cond = (temperature < (temp + 500 )) & (temperature > (temp - 500)) &  (gravity < (g + 1)) & (gravity > (g - 1)) & (metallicity < (z + 1)) & (metallicity > (z - 1))
    stats = np.empty(15)
    for band in range(0,6):
        stats[2*band], stats[2*band+1] = np.std(output[:,band]), stat.skew(output[:,band])
    stats[12], stats[13], stats[14] = temp, g, z
    print >>stats_file, stats[0],stats[1],stats[2],stats[3],stats[4],stats[5],stats[6],stats[7],stats[8],stats[9],stats[10],stats[11],stats[12],stats[13],stats[14]
