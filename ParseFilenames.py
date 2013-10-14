import re
import os
listing = os.listdir("/Volumes/Le Drive/Spectra")
pat_txt = re.compile('k([m,p])([0-9]+)_([0-9]+).fits_g([0-9]+)')
pat_fits = re.compile('lte([0-9]+)-([0-9]+\.[0-9]+)(\+|-)([0-9]+\.[0-9]+).+') #Temperature, gravity, metallicity
outFile = open("FilenameData.txt" , 'w')
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
    if m or n:
        print >>outFile,  filename, temp, g, z
