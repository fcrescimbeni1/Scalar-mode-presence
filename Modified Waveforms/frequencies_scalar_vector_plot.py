from pycbc import conversions as cn
import qnm 
import numpy as np
import matplotlib.pyplot as plt

#qnm.download_data()

#parameters
final_mass=62

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

#-----------------SPIN SEQUENCE--------------------#
  
f = open("sequence_GR_220.txt", "w")

#GR 220 mode
grav_220 = qnm.modes_cache(s=-2,l=2,m=2,n=0)

for i in range(0,1000,1):
    a_i = i/1000
    omega, A, C = grav_220(a=a_i)
    re_om=np.real(omega)
    im_om=np.imag(omega)
    f.write(str(a_i) + '\t' + str(re_om) + '\t' + str(im_om) + '\n')
    
f = open("sequence_GR_221.txt", "w")

#GR 221 mode
grav_221 = qnm.modes_cache(s=-2,l=2,m=2,n=1)

for i in range(0,1000,1):
    a_i = i/1000
    omega, A, C = grav_221(a=a_i)
    re_om=np.real(omega)
    im_om=np.imag(omega)
    f.write(str(a_i) + '\t' + str(re_om) + '\t' + str(im_om) + '\n')
    
f = open("sequence_S_220.txt", "w")

#scalar 220 mode
grav_220_s = qnm.modes_cache(s=0,l=2,m=2,n=0)

for i in range(0,1000,1):
    a_i = i/1000
    omega, A, C = grav_220_s(a=a_i)
    re_om=np.real(omega)
    im_om=np.imag(omega)
    f.write(str(a_i) + '\t' + str(re_om) + '\t' + str(im_om) + '\n') 
f.close()
    
f = open("sequence_V_220.txt", "w")

#vector 220 mode
grav_220_v = qnm.modes_cache(s=-1,l=2,m=2,n=0)

for i in range(0,1000,1):
    a_i = i/1000
    omega, A, C = grav_220_v(a=a_i)
    re_om=np.real(omega)
    im_om=np.imag(omega)
    f.write(str(a_i) + '\t' + str(re_om) + '\t' + str(im_om) + '\n')    
f.close() 

#--------------------PLOTS----------------------#

a_GR0, re_om_GR0, im_om_GR0 = np.loadtxt("sequence_GR_220.txt", usecols=(0,1,2), unpack=True)
a_GR1, re_om_GR1, im_om_GR1 = np.loadtxt("sequence_GR_221.txt", usecols=(0,1,2), unpack=True)
a_S0, re_om_S0, im_om_S0 = np.loadtxt("sequence_S_220.txt", usecols=(0,1,2), unpack=True)
a_V0, re_om_V0, im_om_V0 = np.loadtxt("sequence_V_220.txt", usecols=(0,1,2), unpack=True)

#frequencies and damping times
#GR 220
f_GR0=f_to_Phys(re_om_GR0,final_mass)/(2*np.pi)
tau_GR0=-1e3/f_to_Phys(im_om_GR0,final_mass)

#GR 221
f_GR1=f_to_Phys(re_om_GR1,final_mass)/(2*np.pi)
tau_GR1=-1e3/f_to_Phys(im_om_GR1,final_mass)

#scalar 220
f_S0=f_to_Phys(re_om_S0,final_mass)/(2*np.pi)
tau_S0=-1e3/f_to_Phys(im_om_S0,final_mass)

#vector 220
f_V0=f_to_Phys(re_om_V0,final_mass)/(2*np.pi)
tau_V0=-1e3/f_to_Phys(im_om_V0,final_mass)

plt.figure(figsize=(14, 6))

#re om
plt.subplot(121)
plt.plot(a_GR0, f_GR0, label="220, grav", color="black", linestyle="-", linewidth=1)
plt.plot(a_GR1, f_GR1, label="221, grav", color="blue", linestyle="--", linewidth=1)
plt.plot(a_S0, f_S0, label="Scalar, 220", color="orange", linestyle="--", linewidth=2.5)
plt.plot(a_V0, f_V0, label="Vector, 220", color="green", linestyle="--", linewidth=2.5)
plt.xlabel('$a_f$')
plt.ylabel('$f [Hz]$')
plt.legend()

#im om
plt.subplot(122)
plt.plot(a_GR0, tau_GR0, label="220, grav", color="black", linestyle="-", linewidth=1)
plt.plot(a_GR1, tau_GR1, label="221, grav", color="blue", linestyle="--", linewidth=1)
plt.plot(a_S0, tau_S0, label="Scalar, 220", color="orange", linestyle="--", linewidth=2.5)
plt.plot(a_V0, tau_V0, label="Vector, 220", color="green", linestyle="--", linewidth=2.5)
plt.xlabel('$a_f$')
plt.ylabel(r'$\tau [ms]$')
plt.legend()

plt.savefig("frequencies_damping_GR_scalar_vector.png")
