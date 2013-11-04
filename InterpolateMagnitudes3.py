import numpy as np
import scipy.interpolate as interpolate
import scipy.stats as stat

def InterpolateMagnitudes(data, temp_grid, metallicity_grid, gravity_grid, a0_grid):
    eval_grid = np.meshgrid(temp_grid, gravity_grid, metallicity_grid,a0_grid)
    eval_points = np.empty((len(np.ravel(eval_grid[0])),4))
    eval_points[:,0], eval_points[:,1], eval_points[:,2], eval_points[:,3] = np.ravel(eval_grid[0]), np.ravel(eval_grid[1]), np.ravel(eval_grid[2]), np.ravel(eval_grid[3])
    points = np.empty((len(data[:,1]),4))
    points[:,0], points[:,1], points[:,2], points[:,3] = data[:,7], data[:,8], data[:,9], data[:,10]
    mags = np.empty((len(eval_points[:,0]),6))
    for band in range(1,7):
        values = data[:,band]
        mags[:,band-1] = interpolate.griddata(points, values, eval_points)
    temperature, gravity, metallicity, a0 = eval_points[:,0], eval_points[:,1], eval_points[:,2], eval_points[:,3]
    return(mags, temperature, gravity, metallicity, a0)

dataDict = {"Gaia_G_mag":0, "LSST_U_Mag":1,  "LSST_G_Mag":2,  "LSST_R_Mag":3,  "LSST_I_Mag":4,  "LSST_Z_Mag":5,  "LSST_Y4_Mag":6, "T":7, "G":8, "9":9}
pointsDict = {"T":0, "G":1, "Z":2}
data_file = np.loadtxt('Mags_g.txt')
points_file = np.loadtxt('SamplePoints.txt')
stats_file = open("InterpStats.txt" , 'w')
print >>stats_file, '# LSST_U_Mag_SD LSST_U_Mag_Skew LSST_G_Mag_SD LSST_G_Mag_Skew LSST_R_Mag_SD LSST_R_Mag_Skew LSST_I_Mag_SD LSST_I_Mag_Skew LSST_Z_Mag_SD LSST_Z_Mag_Skew LSST_Y4_Mag_SD LSST_Y4_Mag_Skew Temperature Gravity Metallicity'
for count in range(0,len(points_file[:,0])):
    temp = points_file[count,0]
    z = points_file[count,2]
    g = points_file[count,1]
    a0 = points_file[count, 3]
    temp_grid = np.arange(temp-200.,temp+200.,20.)#2300 to 12000, Variation: 200
    metallicity_grid = np.arange(z-.3,z+.3,.05)#-4 to 1, Variation: .3
    gravity_grid = np.arange(g-.2,g+.2,.05)#0 to 7, Variation: .2
    a0_grid =  gravity_grid = np.arange(a0+.5,a0-.5,.05)
    mags, temperature, gravity, metallicity, a0 = InterpolateMagnitudes(data_file, temp_grid, metallicity_grid, gravity_grid,a0_grid)
    output = np.empty((len(temperature),10))
    output[:,0:6], output[:,6], output[:,7], output[:,8], output[:,9]= mags[:,0:6], temperature, gravity, metallicity, a0
    np.savetxt('interp_'+str(temp)+"_"+str(z)+"_"+str(g)+'.txt', output, header = 'LSST_U_Mag LSST_G_Mag LSST_R_Mag LSST_I_Mag LSST_Z_Mag LSST_Y4_Mag Temperature Gravity Metallicity a0')
    stats = np.empty(15)
    for band in range(0,6):
        stats[2*band], stats[2*band+1] = np.std(output[:,band]), stat.skew(output[:,band])
    stats[12], stats[13], stats[14] = temp, g, z
    print >>stats_file, stats[0],stats[1],stats[2],stats[3],stats[4],stats[5],stats[6],stats[7],stats[8],stats[9],stats[10],stats[11],stats[12],stats[13],stats[14]