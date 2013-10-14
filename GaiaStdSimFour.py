import numpy as np
from Bandpass import Bandpass
from Sed import Sed
import GaiaSimulatorThree
import os
import re
import time
import pyfits
import fnmatch
def ImportSED(filename,d_lambda):
    sed = Sed()
    sed.readSED_flambda(filename)
    sed.synchronizeSED(wavelen_step = d_lambda)
    return(sed)
def ImportSEDfits(filename):
    sed = Sed()
    fits = pyfits.open(filename)
    crdelt = fits[0].header['CDELT1'] * .1 #Converts Angstroms to nanometers
    crval = fits[0].header['CRVAL1'] * .1 #same
    length = len(fits[0].data)
    wavelen = np.arange(crval,crval+length*crdelt,crdelt)
    sed.setSED(wavelen, fits[0].data)
    return(sed)
def SimulateLSST(throughputs, throughputs_location, sed):
    bandpass = Bandpass()
    bandpass.readThroughputList(throughputs, throughputs_location)
    return(sed.calcMag(bandpass))   
def GetMags(sed_name,data_path):
    if fnmatch.fnmatch(sed_name, '*PHOENIX*'):
        sed = ImportSEDfits(sed_name)
    else:
        sed = ImportSED(sed_name,.01)
    LSST_bands = ['total_u.dat', 'total_g.dat', 'total_r.dat', 'total_i.dat', 'total_z.dat', 'total_y.dat']
    LSST_mags = np.empty(6)
    for band in range(0,6):
        LSST_mags[band] = SimulateLSST([LSST_bands[band]],data_path+'Throughputs', sed)
    Gaia_G_mag = GaiaSimulatorThree.SimulateGaiaG(['Gaia_G.txt'], data_path+'Throughputs', sed)
    return(Gaia_G_mag, LSST_mags)

#@profile
def RunSEDs(outFileName, dataPath='/Users/fluffy/Documents/workspace/AstronomyProject/data/', SEDPath='/home/fluffy/workspace/GaiaSims/phoenix'):
    listing = os.listdir(SEDPath)
    length=len(listing)
    start_time = time.time()
    pat_txt = re.compile('k([m,p])([0-9]+)_([0-9]+).fits_g([0-9]+)')
    pat_fits = re.compile('lte([0-9]+)-([0-9]+\.[0-9]+)(\+|-)([0-9]+\.[0-9]+).+') #Temperature, gravity, metallicity
    outFile = open(outFileName , 'w')
    print >>outFile, '#Gaia_G_mag LSST_U_Mag LSST_G_Mag LSST_R_Mag LSST_I_Mag LSST_Z_Mag LSST_Y4_Mag Temperature Gravity Metallicity'
    count = 0
    for filename in listing:
        m = pat_txt.match(filename)
        n = pat_fits.match(filename)
        if m:
            if(m.group(1) == 'm'):
                mp = -1
            else:
                mp = 1
            z = float(m.group(2)) * mp
            temp = float(m.group(3))
            g = float(m.group(4))
        elif n:
            if(n.group(3) == '+'):
                mp = 1
            else:
                mp = -1
            z = float(n.group(4)) * mp
            temp = float(n.group(1))
            g = float(n.group(2))
        if (m or n) and not fnmatch.fnmatch(filename, "*Alpha*"):
            Gaia_g_mag, LSST_mags = GetMags(SEDPath +"/"+ filename, dataPath)
            print >>outFile,  Gaia_g_mag, LSST_mags[0]-Gaia_g_mag, LSST_mags[1]-Gaia_g_mag, LSST_mags[2]-Gaia_g_mag, LSST_mags[3]-Gaia_g_mag, LSST_mags[4]-Gaia_g_mag, LSST_mags[5]-Gaia_g_mag, temp, g, z
        count = count + 1
        if count%10 == 0:
            print((time.time()-start_time) * ((float(length)/float(count)) - 1))
    print(time.time() - start_time)
    
if __name__ == '__main__':
    RunSEDs('Mags_g.txt', SEDPath= '/Volumes/Le Drive/Spectra')