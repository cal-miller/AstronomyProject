import numpy as np
import os
import re
pat = re.compile("interp_([0-9]+).0_-([0-9].[0-9])_([0-9].[0-9]+)_0.5.*")
listing = os.listdir("/Users/fluffy/Documents/workspace/AstronomyProject/src/")
for file in listing:
    m = pat.match(file)
    if(m):
        a = np.loadtxt(file)
        t = float(m.group(1))
        g = float(m.group(2))
        z = float(m.group(3))
        cond = a == t
        cond2 = a == g
        cond3 = a == z
        a = a[np.extract(a[:,7],cond)]
        print(a[:,7])