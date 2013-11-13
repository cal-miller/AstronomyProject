import numpy as np
import scipy as sp
import scipy.interpolate as interp
import scipy.stats as stats
import matplotlib.pyplot as plt
import time


#Loads files
points = np.loadtxt("SamplePoints.txt")
data = np.loadtxt("Mags_g.txt")
stats_file = open("InterpStats.txt" , 'w')

#Breaks data into programmer-readable chunks
mags, t, g, z, a0 = data[:,0:7], data[:,7], data[:,8], data[:,9], data[:,10]
interp_points = np.empty((len(data[:,1]),4))
interp_points[:,0], interp_points[:,1], interp_points[:,2], interp_points[:,3] = t,g,z,a0


#Iterates through list of points to center interpolation around
start_time = time.time()
for point in points:
    t_point, g_point, z_point, a0_point = point[0], point[1], point[2], point[3]

    
    #Defines range of coordinates of points at which to interpolate
    temp_grid = np.arange(t_point-200.,t_point+200.,20.)#2300 to 12000, Variation: 200
    metallicity_grid = np.arange(z_point-.3,z_point+.3,.05)#-4 to 1, Variation: .3
    gravity_grid = np.arange(g_point-.2,g_point+.2,.05)#0 to 7, Variation: .2
    a0_grid = np.arange(0,.2,.005)#0 to 1
    
    #Does nasty array stuff to prepare data for interpolation
    eval_grid = np.meshgrid(temp_grid, gravity_grid, metallicity_grid, a0_grid)
    eval_points = np.zeros((len(np.ravel(eval_grid[0])),4))
    eval_points[:,0], eval_points[:,1], eval_points[:,2], eval_points[:,3] = np.ravel(eval_grid[0]), np.ravel(eval_grid[1]), np.ravel(eval_grid[2]), np.ravel(eval_grid[3])
    out = np.empty((11,len(eval_points))); 
       
    #Actually interpolates each band
    for band in range(0,7):
        interpolated = interp.griddata(interp_points, mags[:,band], eval_points)
        out[band,:] = interpolated
    
    #Outputs results
    out[7], out[8], out[9], out[10] = eval_points[:,0], eval_points[:,1], eval_points[:,2], eval_points[:,3]
    np.savetxt('interp_'+str(t_point)+"_"+str(z_point)+"_"+str(g_point)+"_"+str(a0_point)+'.txt', np.transpose(out),header = 'Gaia_G_Mag LSST_U_Mag LSST_G_Mag LSST_R_Mag LSST_I_Mag LSST_Z_Mag LSST_Y4_Mag Temperature Gravity Metallicity a0')
    print(time.time()-start_time)