from pycbc import conversions as cn
import qnm 
import numpy as np
import matplotlib.pyplot as plt

#qnm.download_data()

#parameters
final_mass=100
final_spin=0.6

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

#--------------------GW---------------------#

print("\ns=-2 (Gravitational Wave):\n")

#---------------PyCBC section---------------#

tau220=cn.tau_from_final_mass_spin(final_mass, final_spin, l=2, m=2, n=0)
f220=cn.freq_from_final_mass_spin(final_mass, final_spin, l=2, m=2, n=0)
tau221=cn.tau_from_final_mass_spin(final_mass, final_spin, l=2, m=2, n=1)
f221=cn.freq_from_final_mass_spin(final_mass, final_spin, l=2, m=2, n=1)

print("\nPyCBC:\n")
print("f220: {0:.5f}Hz".format(f220))
print("tau220: {0:.5f}s".format(tau220))
print("f221: {0:.5f}Hz".format(f221))
print("tau221: {0:.5f}s".format(tau221))

#----------------qnm section--------------------#

#220
grav_220 = qnm.modes_cache(s=-2,l=2,m=2,n=0)
omega220, A, C = grav_220(a=final_spin)
f220=f_to_Phys(np.real(omega220),final_mass)/(2*np.pi)
tau220=-1/f_to_Phys(np.imag(omega220),final_mass)

#221
grav_221 = qnm.modes_cache(s=-2,l=2,m=2,n=1)
omega221, A, C = grav_221(a=final_spin)
f221=f_to_Phys(np.real(omega221),final_mass)/(2*np.pi)
tau221=-1/f_to_Phys(np.imag(omega221),final_mass)

print("\nqnm:\n")
print("f220: {0:.5f}Hz".format(f220))
print("tau220: {0:.5f}s".format(tau220))
print("f221: {0:.5f}Hz".format(f221))
print("tau221: {0:.5f}s".format(tau221))


#------------------SCALAR FIELD----------------#

print("\ns=0 (Scalar field):\n")

#220
grav_220 = qnm.modes_cache(s=0,l=2,m=2,n=0)
omega220, A, C = grav_220(a=final_spin)
f220_s=f_to_Phys(np.real(omega220),final_mass)/(2*np.pi)
tau220_s=-1/f_to_Phys(np.imag(omega220),final_mass)
delta_f220=f220_s/f220-1
delta_tau220=tau220_s/tau220-1

#221
grav_221 = qnm.modes_cache(s=0,l=2,m=2,n=1)
omega221, A, C = grav_221(a=final_spin)
f221_s=f_to_Phys(np.real(omega221),final_mass)/(2*np.pi)
tau221_s=-1/f_to_Phys(np.imag(omega221),final_mass)
delta_f221=f221_s/f221-1
delta_tau221=tau221_s/tau221-1


print("f220: {0:.5f}Hz".format(f220_s))
print("tau220: {0:.5f}s".format(tau220_s))
print("f221: {0:.5f}Hz".format(f221_s))
print("tau221: {0:.5f}s".format(tau221_s))
print("delta_f220: {0:.2f}", delta_f220)
print("delta_tau220: {0:.2f}", delta_tau220)
print("delta_f221: {0:.2f}", delta_f221)
print("delta_tau221: {0:.2f}", delta_tau221)
print("\n")

#-----------------SPIN SEQUENCE--------------------#

s, l, m, n = (-2, 2, 2, 1)
mode_list = [(s, l, m, n)]
modes = { ind : qnm.modes_cache(*ind) for ind in mode_list }

for mode, seq in modes.items():
    re_om=np.real(seq.omega)
    im_om=np.imag(seq.omega)
    
s, l, m, n = (0, 2, 2, 0)
mode_list = [(s, l, m, n)]
modes = { ind : qnm.modes_cache(*ind) for ind in mode_list }

for mode, seq in modes.items():
    re_om_s=np.real(seq.omega)
    im_om_s=np.imag(seq.omega)

#spin array
spins = np.linspace(0, 0.99, len(re_om))

#data stack
data = np.column_stack((spins, re_om, im_om))

#save txt
np.savetxt('geometric_frequencies_GR.txt', data, fmt='%.4f', delimiter='\t')

#spin array
spins = np.linspace(0, 0.99, len(re_om_s))

#data stack
data = np.column_stack((spins, re_om_s, im_om_s))

#save txt
np.savetxt('geometric_frequencies_scalar.txt', data, fmt='%.4f', delimiter='\t')

#-----------------SPIN SEQUENCE v2--------------------#

f = open("sequence_GW.txt", "w")

#GW mode
grav_221 = qnm.modes_cache(s=-2,l=2,m=2,n=1)

for i in range(0,1000,1):
    a_i = i/1000
    omega, A, C = grav_221(a=a_i)
    re_om=np.real(omega)
    im_om=np.imag(omega)
    f.write(str(a_i) + '\t' + str(re_om) + '\t' + str(im_om) + '\n')
    
f = open("sequence_scalar.txt", "w")

#scalar mode
grav_220_s = qnm.modes_cache(s=0,l=2,m=2,n=1)

for i in range(0,1000,1):
    a_i = i/1000
    omega, A, C = grav_220_s(a=a_i)
    re_om=np.real(omega)
    im_om=np.imag(omega)
    f.write(str(a_i) + '\t' + str(re_om) + '\t' + str(im_om) + '\n')
    
f = open("sequence_vector.txt", "w")

#scalar mode
grav_220_v = qnm.modes_cache(s=1,l=2,m=2,n=1)

for i in range(0,1000,1):
    a_i = i/1000
    omega, A, C = grav_220_v(a=a_i)
    re_om=np.real(omega)
    im_om=np.imag(omega)
    f.write(str(a_i) + '\t' + str(re_om) + '\t' + str(im_om) + '\n')
    

