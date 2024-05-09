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

#--------------------------------MODIFED WAVEFORM--------------------------------#

def modified_TdQNMfromMassSpin(**args):
    
    #Required parameters
    final_mass = args['final_mass']
    final_spin = args['final_spin']
    amp220 = args['amp220']
    amp221 = args['amp221']
    phi220 = args['phi220']
    phi221 = args['phi221']
    distance = args['distance']
    inclination = args['inclination']
    f_lower = args['f_lower']
    delta_t = args['delta_t']
    lmns = args['lmns']
    
    #read txt files
    a, re_om, im_om = np.loadtxt("sequence_GW.txt", usecols=(0,1,2), unpack=True)
    a, re_om_s, im_om_s = np.loadtxt("sequence_scalar.txt", usecols=(0,1,2), unpack=True)
    
    #minimum index
    min_index = np.argmin(np.abs(a - abs(final_spin)))

    #print
    print("Nearest value:", a[min_index])
    print("Relative index:", min_index)
    
    #GW mode
    f221=f_to_Phys(re_om[min_index],final_mass)/(2*np.pi)
    tau221=-1/f_to_Phys(im_om[min_index],final_mass)
    
    #scalar mode
    f221_s=f_to_Phys(re_om_s[min_index],final_mass)/(2*np.pi)
    tau221_s=-1/f_to_Phys(im_om_s[min_index],final_mass)
    
    #additional parameters
    delta_f221=f221_s/f221-1
    delta_tau221=tau221_s/tau221-1 
    
    #print deviations
    print("delta_f221: ", delta_f221)
    print("delta_tau221: ", delta_tau221)
    
    #waveform with 221 mode as 220 scalar
    hp, hc = wf0(final_mass=final_mass, final_spin=final_spin, amp220=amp220, amp221=amp221, phi220=phi220, phi221=phi221, distance=distance, inclination=inclination, lmns=lmns, f_lower=f_lower, delta_t=delta_t, delta_f221=delta_f221, delta_tau221=delta_tau221)
    return hp, hc


# This tells pycbc about our new waveform so we can call it from standard
# pycbc functions. If this were a frequency-domain model, select 'frequency'
# instead of 'time' to this function call.
pycbc.waveform.add_custom_waveform('modified_TdQNMfromMassSpin', modified_TdQNMfromMassSpin, 'time', force=True)

#plot
hp, hc = pycbc.waveform.get_td_waveform(approximant="modified_TdQNMfromMassSpin", final_mass=100, final_spin=0.6, amp220=0.15, amp221=1.5, phi220=2, phi221=0.23, distance=10, inclination=0.26, lmns=["222"], f_lower=20, delta_t=1/(4096*4))


plt.figure(0)
plt.plot(hp.sample_times, hp, label="Plus polarization")
plt.plot(hc.sample_times, hc, label="Cross polarization")
plt.xlabel('Time (s)')
plt.ylabel('Ringdown polarizations')
plt.title("Modified Ringdown Waveform")
plt.legend()
plt.savefig("modified_TdQNMFromMassSpin.png")

#---------------------------comparison with GR-----------------------------#
hp_GR, hc_GR = wf0(final_mass=100, final_spin=0.6, amp220=0.15, amp221=0.42, phi220=2, phi221=0.23, delta_f221=0, delta_tau221=0, distance=10, inclination=0.26, lmns=["222"], f_lower=20, delta_t=1/(4096*4))

fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(10,4))

#plus
ax1.plot(hp_GR.sample_times, hp_GR, label="GR plus polarization", color="red")
ax1.plot(hp.sample_times, hp, label="Beyond GR plus polarization", color="blue", linestyle="--")
ax1.set_xlabel('Time (s)')
ax1.set_title("Plus polarizations")
ax1.legend()

#cross
ax2.plot(hc_GR.sample_times, hc_GR, label="GR cross polarization", color="red")
ax2.plot(hc.sample_times, hc, label="Beyond GR cross polarization", color="blue", linestyle="--")
ax2.set_xlabel('Time (s)')
ax2.set_title("Cross polarizations")
ax2.legend()

plt.savefig("GR_and_Beyond.png")
