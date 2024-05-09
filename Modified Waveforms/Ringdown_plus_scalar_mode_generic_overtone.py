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
a, re_om_s, im_om_s = np.loadtxt("sequence_scalar.txt", usecols=(0,1,2), unpack=True)

def TdQNMfromFinalMassSpin_SD_generic_overtone(**args):
    
    #Required parameters
    final_mass = args['final_mass']
    final_spin = args['final_spin']
    
    #overtone-dependent parameters
    lmns = [str(args['lmns'])]
    #print(lmns)
    n_overtones = lmns[0][2]
    n = int(n_overtones)-1
    
    #minimum index
    min_index = np.argmin(np.abs(a - abs(final_spin)))
    
    #GW mode
    f_GW,tau_GW=cn.get_lm_f0tau(mass=final_mass, spin=final_spin, l=2, m=2, n=n, which='both')
    
    #n=0 scalar mode
    f220_s=f_to_Phys(re_om_s[min_index],final_mass)/(2*np.pi)
    tau220_s=-1/f_to_Phys(im_om_s[min_index],final_mass)
    
    #additional parameters
    delta_f=f220_s/f_GW-1
    delta_tau=tau220_s/tau_GW-1
    
    #save in args
    s_f="delta_f22"+str(n)
    s_tau="delta_tau22"+str(n)
    args[s_f]=delta_f
    args[s_tau]=delta_tau
    
    """
    #print deviations
    print(s_f, ": ", delta_f)
    print(s_tau, ": ", delta_tau)
    """
    
    #waveform with 221 mode as 220 scalar
    hp, hc = wf0(**args)
    return hp, hc
"""
#TESTS
print("222")
hp, hc = TdQNMfromFinalMassSpin_SD(approximant="test", final_mass=70, final_spin=0.6, amp220=0.05, amp221=0.42, phi220=2, phi221=0.23, distance=10, inclination=0.26, lmns=["222"], f_lower=20, delta_t=1/(4096*4), toffset=0.002, f_ref=20, t_final=2, harmonics="spheroidal")

print("223")
hp, hc = TdQNMfromFinalMassSpin_SD(approximant="test", final_mass=70, final_spin=0.6, amp220=0.05, amp221=0.42, amp222=0.8, phi220=2, phi221=0.23, phi222=0.5, distance=10, inclination=0.26, lmns=["223"], f_lower=20, delta_t=1/(4096*4), toffset=0.002, f_ref=20, t_final=2, harmonics="spheroidal")
"""