import numpy as np
import qnm
import matplotlib.pyplot as plt
import pycbc.waveform
from pycbc.types import TimeSeries
from pycbc.waveform.ringdown import get_td_from_final_mass_spin as wf0
from pycbc import conversions as cn
#import sequence_GW.txt
#import sequence_scalar.txt

#conversions
c=2.99792458e8 #m
G=6.67259e-11 #m^3/(kg*s^2)
pc=3.0857e16
Msol=1.9885e30 #kg
cf=7.4247138240457957979e-28

def f_to_Phys(f,M):
    """ It converts NR frequencies to physical units in [Hz].
    """  
    return (c**3/(M*Msol*G))*f

#--------------------------------MODIFIED WAVEFORM--------------------------------#

#save list in cache
a, re_om, im_om = np.loadtxt("sequence_GW.txt", usecols=(0,1,2), unpack=True)
a, re_om_s, im_om_s = np.loadtxt("sequence_scalar.txt", usecols=(0,1,2), unpack=True)

def TdQNMfromFinalMassSpin_SD(**args):
    
    #Required parameters
    final_mass = args['final_mass']
    final_spin = args['final_spin']
    amp220 = args['amp220']
    amp221 = args['amp221']
    phi220 = args['phi220']
    phi221 = args['phi221']
    distance = args['distance']
    inclination = args['inclination']
    #polarization = args['polarization']
    toffset = args["toffset"]
    #ra = args['ra']
    #dec = args['dec']
    f_ref = args['f_ref']
    #tc = args["tc"]
    t_final = args["t_final"]
    harmonics = args["harmonics"]
    f_lower = args['f_lower']
    delta_t = args['delta_t']
    lmns = args['lmns']
    
    #read txt files
    #a, re_om, im_om = np.loadtxt("sequence_GW.txt", usecols=(0,1,2), unpack=True)
    #a, re_om_s, im_om_s = np.loadtxt("sequence_scalar.txt", usecols=(0,1,2), unpack=True)
    
    #minimum index
    min_index = np.argmin(np.abs(a - abs(final_spin)))

    #print
    #print("Nearest value:", a[min_index])
    #print("Relative index:", min_index)
    
    #GW mode
    f221=f_to_Phys(re_om[min_index],final_mass)/(2*np.pi)
    tau221=-1/f_to_Phys(im_om[min_index],final_mass)
    
    #scalar mode
    f220_s=f_to_Phys(re_om_s[min_index],final_mass)/(2*np.pi)
    tau220_s=-1/f_to_Phys(im_om_s[min_index],final_mass)
    
    #additional parameters
    delta_f221=f220_s/f221-1
    delta_tau221=tau220_s/tau221-1 
    
    #print deviations
    #print("delta_f221: ", delta_f221)
    #print("delta_tau221: ", delta_tau221)
    
    #waveform with 221 mode as 220 scalar
    hp, hc = wf0(final_mass=final_mass, final_spin=final_spin, amp220=amp220, amp221=amp221, phi220=phi220, phi221=phi221, distance=distance, inclination=inclination, lmns=lmns, f_lower=f_lower, delta_t=delta_t, delta_f221=delta_f221, delta_tau221=delta_tau221, harmonics=harmonics, toffset=toffset, t_final=t_final, f_ref=f_ref)
    return hp, hc
"""
hp, hc = TdQNMfromFinalMassSpin_SD(approximant="test", final_mass=70, final_spin=0.6, amp220=0.05, amp221=0.42, phi220=2, phi221=0.23, distance=10, inclination=0.26, lmns=["222"], f_lower=20, delta_t=1/(4096*4), toffset=0.002, f_ref=20, t_final=2, harmonics="spheroidal")
"""