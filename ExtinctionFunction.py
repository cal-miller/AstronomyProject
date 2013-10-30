"""
Extinction function as used by Bailer-Jones(2011), in turn based on
Cardelli et al(1988).

Valid for x < 5.9 (wl > 170 nm)

wl is in nm

extinction is in magnitudes
transmission is 0-1

For our program, a0 < 1
increment by .1
r = 3.1
"""

def extinction(wl, a0, r):
    x = 1000./wl
    a = 1.802 - 0.316*x - 0.104/((x-4.67)**2 + 0.341)
    b = -3.090 + 1.825*x + 1.206/((x-4.62)**2 + 0.263)

    return a0*(a + b/r)

def transmission(wl, a0, r):
    return 10.0**(-0.4*extinction(wl, a0, r))
