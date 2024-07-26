import numpy as np
import qnm
import matplotlib.pyplot as plt
import pycbc.waveform
import pykerr
from pycbc.types import TimeSeries
from pycbc.waveform.ringdown import get_td_from_final_mass_spin as wf0
from pycbc import conversions as cn

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

def TdQNMfromFinalMassSpin_SD_pk(**args):
    
    #Required parameters
    final_mass = args['final_mass']
    final_spin = args['final_spin']
    
    #overtone-dependent parameters
    lmns = [str(args['lmns'])]
    #print(lmns)
    n_overtones = lmns[0][2]
    n = int(n_overtones)-1
    
    #GRn mode
    f_GRn=pykerr.qnmfreq(final_mass, final_spin, l=2, m=2, n=n)
    tau_GRn=pykerr.qnmtau(final_mass, final_spin, l=2, m=2, n=n)
    
    #n=0 scalar mode
    f220_s=pykerr.qnmfreq(final_mass, final_spin, l=2, m=2, n=0, driven="sd")
    tau220_s=pykerr.qnmtau(final_mass, final_spin, l=2, m=2, n=0, driven="sd")
    
    #additional parameters
    delta_f=f220_s/f_GRn-1
    delta_tau=tau220_s/tau_GRn-1
    
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
    
    #waveform with 22n mode as 220 scalar
    hp, hc = wf0(**args)
    return hp, hc
"""
#TESTS
print("222")
hp, hc = TdQNMfromFinalMassSpin_SD_pk(approximant="test", final_mass=70, final_spin=0.6, amp220=0.05, amp221=0.42, phi220=2, phi221=0.23, distance=10, inclination=0.26, lmns=["222"], f_lower=20, delta_t=1/(4096*4), toffset=0.002, f_ref=20, t_final=2, harmonics="spheroidal")

print("223")
hp, hc = TdQNMfromFinalMassSpin_SD_pk(approximant="test", final_mass=70, final_spin=0.6, amp220=0.05, amp221=0.42, amp222=0.8, phi220=2, phi221=0.23, phi222=0.5, distance=10, inclination=0.26, lmns=["223"], f_lower=20, delta_t=1/(4096*4), toffset=0.002, f_ref=20, t_final=2, harmonics="spheroidal")
"""