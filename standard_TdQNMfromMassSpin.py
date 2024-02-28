import numpy
import qnm
import matplotlib.pyplot as plt
import pycbc.waveform
from pycbc.types import TimeSeries
from pycbc.waveform.ringdown import get_td_from_final_mass_spin as wf0

def test_waveform(**args):
    
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
    delta_f221 = args['delta_f221']
    delta_tau221 = args['delta_tau221']
    
    hp, hc = wf0(final_mass=final_mass, final_spin=final_spin, amp220=amp220, amp221=amp221, phi220=phi220, phi221=phi221, distance=distance, inclination=inclination, lmns=lmns, f_lower=f_lower, delta_t=delta_t, delta_f221=delta_f221, delta_tau221=delta_tau221)
    return hp, hc


# This tells pycbc about our new waveform so we can call it from standard
# pycbc functions. If this were a frequency-domain model, select 'frequency'
# instead of 'time' to this function call.
pycbc.waveform.add_custom_waveform('test', test_waveform, 'time', force=True)

#plot
hp, hc = pycbc.waveform.get_td_waveform(approximant="test", final_mass=100, final_spin=0.6, amp220=0.15, amp221=0.42, phi220=2, phi221=0.23, delta_f221=0, delta_tau221=0, distance=10, inclination=0.26, lmns=["222"], f_lower=20, delta_t=1/(4096*4))


plt.figure(0)
plt.plot(hp.sample_times, hp, label="Plus polarization")
plt.plot(hc.sample_times, hc, label="Cross polarization")
plt.xlabel('Time (s)')
plt.ylabel('Ringdown polarizations')
plt.title("Standard Ringdown Waveform")
plt.legend()
plt.savefig("standard_TdQNMFromMassSpin.png")