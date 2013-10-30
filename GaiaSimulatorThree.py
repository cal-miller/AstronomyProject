"""
Imports a spectrum, imports an instrument's bandpasses.
Applies the bandpasses to the spectrum and convolves the spectrum with a gaussian kernel to simulate the output
from the telescope.
Plots the output and saves it to a text file
Requires:
    numpy, Bandpass, Sed
Inputs:
    red_throughputs:  List of all the throughputs for the red spectrometer
    blue_throughputs: List of all the throughputs for the blue spectrometer
    throughputs_location: Address of  directory containing throughput
    sigma: width of gaussian kernel
    sed: sed object
Outputs:
    gaia_out_red: red spectrum
    gaia_out_blue: blue spectrum
"""
from matplotlib import pyplot as plt
import numpy as np
import scipy as sp
from Bandpass import Bandpass
from Sed import Sed
def GenerateNoise(sb, level):
    noise = np.random.randn(len(sb)) * level + 1
    return(sb*noise)
#@profile
def SimulateGaia(throughputs, throughputs_location, sigma, sed):
    d_lambda = 1 #Wavelength resolution for convolution
    def gaussian(x, sigma):
        y = 1.0/(sigma*np.sqrt(2.0*np.pi))*np.exp(-(x*x)/(2.0*sigma*sigma))
        return y
    bandpass = Bandpass()
    bandpass.readThroughputList(throughputs,throughputs_location)
    (wavelen,energy) = sed.getSED_flambda()
    photons = energy*wavelen / 1.989e-9
    (wavelen,photons) = bandpass.multiplyThroughputs(wavelen,photons)
    wavelength_array = np.arange(-1000, 1000, d_lambda)
    convolve_array = gaussian(wavelength_array,sigma)
    photons_convolved = np.convolve(photons,convolve_array,'same')
    gaia_out = np.empty((len(wavelen),2))
    gaia_out[:,0], gaia_out[:,1] = wavelen, photons_convolved
    gaia_out = np.zeros((50,2))
    count = np.zeros(50)
    gaia_out[:,0] = np.arange(250,1050,16)
    bin = np.digitize(wavelen,gaia_out[:,0])
    for (i,f) in enumerate(photons_convolved):
        gaia_out[bin[i]-1,1] += photons_convolved[i]
        count[bin[i]-1] += 1
        #print(i,bin[i])
    count = np.clip(count, 1, 10000)
    gaia_out[:,1] = gaia_out[:,1] / count
#    gaia_out[:,1] = GenerateNoise(gaia_out[:,1],.03)
    gaia_out[:,1] = GenerateNoise(gaia_out[:,1],.001)

    return(gaia_out)

def SimulateGaiaG(throughputs, throughputs_location, sed):
    bandpass = Bandpass()
    bandpass.readThroughputList(throughputs,throughputs_location)
    return(sed.calcMag(bandpass))

def PlotSpectrum(spectrum):
    """
    Plots a spectrum
    
    Requires:
        matplotlib, numpy
    Input:
        spectrum: 2D array of wavelength and photon count
    """
    plt.plot(spectrum[:,0],spectrum[:,1])
    plt.show()
"""
sed1 = Sed()
sed2 = Sed()
sed1.readSED_flambda('C:\\Users\\Cal\\workspace\\AstronomyProject\\kurucz_r_two\\km01_50000.fits_g50')
sed2.readSED_flambda('C:\\Users\\Cal\\workspace\\AstronomyProject\\kurucz_r_two\\kp01_50000.fits_g50')
g1 = SimulateGaia(['gaia_merged.txt'], 'C:\Users\Cal\workspace\AstronomyProject\Throughputs',110,sed1)
g2 = SimulateGaia(['gaia_merged.txt'], 'C:\Users\Cal\workspace\AstronomyProject\Throughputs',110,sed2)
pyplot.plot(g1[:,0],g1[:,1])
pyplot.plot(g2[:,0],g2[:,1])
pyplot.show()
"""
