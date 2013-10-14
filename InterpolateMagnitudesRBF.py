import numpy as np
import scipy as sp
import scipy.interpolate as interpolate
import scipy.stats as stat

def InterpolateMagnitudes(data, temp_grid, metallicity_grid, gravity_grid, temp, g, z):  #Appears to work

    np.set_printoptions(threshold=np.nan)
    eval_grid = np.meshgrid(temp_grid, gravity_grid, metallicity_grid)
    eval_points = np.empty((len(np.ravel(eval_grid[0])),3))
    eval_points[:,0], eval_points[:,1], eval_points[:,2] = np.ravel(eval_grid[0]), np.ravel(eval_grid[1]), np.ravel(eval_grid[2])
    points = np.empty((len(data[:,1]),3))
    points[:,pointsDict["T"]], points[:,pointsDict["G"]], points[:,pointsDict["Z"]] = data[:,7], data[:,8], data[:,9]
    cond = (points[:,pointsDict["T"]] < (temp + 500 )) & (points[:,pointsDict["T"]] > (temp - 500)) &  (points[:,pointsDict["G"]] < (g + 1)) & (points[:,pointsDict["G"]] > (g - 1)) & (points[:,pointsDict["Z"]] < (z + 1)) & (points[:,pointsDict["Z"]] > (z - 1))
    t_scale = float(np.max(points[cond,pointsDict["T"]]) - np.min(points[cond,pointsDict["T"]]))
    g_scale = float(np.max(points[cond,pointsDict["G"]]) - np.min(points[cond,pointsDict["G"]]))
    z_scale = float(np.max(points[cond,pointsDict["Z"]]) - np.min(points[cond,pointsDict["Z"]]))
    mags = np.empty((len(eval_points[:,pointsDict["T"]]),6))
    outfile = open("interp_inputs.txt","w")
    for band in range(0,6):
        values = data[:,band+1]
        print >> outfile, points[cond,pointsDict["T"]]#/t_scale
        print >> outfile, points[cond,pointsDict["G"]]#/g_scale
        print >> outfile, points[cond,pointsDict["Z"]]#/z_scale
        print >> outfile, values[cond]
        interpolated = interpolate.Rbf(points[cond,0]/t_scale, points[cond,1]/g_scale, points[cond,2]/z_scale, values[cond],function= "gaussian")
        #print(interpolate.Rbf(points[cond,0]/t_scale, points[cond,1]/g_scale, points[cond,2]/z_scale, values[cond]).epsilon)
        mags[:,band] = interpolated(eval_points[:,0]/t_scale,eval_points[:,1]/g_scale,eval_points[:,2]/g_scale)
    temperature, gravity, metallicity = eval_points[:,0], eval_points[:,1], eval_points[:,2]
    return(mags, temperature, gravity, metallicity)

dataDict = {"Gaia_G_mag":0, "LSST_U_Mag":1,  "LSST_G_Mag":2,  "LSST_R_Mag":3,  "LSST_I_Mag":4,  "LSST_Z_Mag":5,  "LSST_Y4_Mag":6, "T":7, "G":8, "9":9}
pointsDict = {"T":0, "G":1, "Z":2}
data_file = np.loadtxt('Mags_g.txt')
points_file = np.loadtxt('SamplePoints.txt')
stats_file = open("InterpStatsRBF.txt" , 'w')
print >>stats_file, '# LSST_U_Mag_SD LSST_U_Mag_Skew LSST_G_Mag_SD LSST_G_Mag_Skew LSST_R_Mag_SD LSST_R_Mag_Skew LSST_I_Mag_SD LSST_I_Mag_Skew LSST_Z_Mag_SD LSST_Z_Mag_Skew LSST_Y4_Mag_SD LSST_Y4_Mag_Skew Temperature Gravity Metallicity'
for count in range(0,len(points_file[:,0])):
    temp = points_file[count,0]
    z = points_file[count,2]
    g = points_file[count,1]
    temp_grid = np.arange(temp-200.,temp+200.,20.)#2300 to 12000, Variation: 200
    metallicity_grid = np.arange(z-.3,z+.3,.05)#-4 to 1, Variation: .3
    gravity_grid = np.arange(g-.2,g+.2,.05)#0 to 7, Variation: .2
    mags, temperature, gravity, metallicity = InterpolateMagnitudes(data_file, temp_grid, metallicity_grid, gravity_grid, temp, g, z)
    output = np.empty((len(temperature),9))
    output[:,0:6], output[:,6], output[:,7], output[:,8] = mags[:,0:6], temperature, gravity, metallicity
    np.savetxt('interp_'+str(temp)+"_"+str(z)+"_"+str(g)+'_RBF.txt', output, header = 'LSST_U_Mag LSST_G_Mag LSST_R_Mag LSST_I_Mag LSST_Z_Mag LSST_Y4_Mag Temperature Gravity Metallicity')
    stats = np.empty(15)
    for band in range(0,6):
        stats[2*band], stats[2*band+1] = np.std(output[:,band]), stat.skew(output[:,band])
    stats[12], stats[13], stats[14] = temp, g, z
    print >>stats_file, stats[0],stats[1],stats[2],stats[3],stats[4],stats[5],stats[6],stats[7],stats[8],stats[9],stats[10],stats[11],stats[12],stats[13],stats[14]