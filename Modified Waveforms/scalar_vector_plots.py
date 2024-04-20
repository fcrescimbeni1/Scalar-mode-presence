from pycbc import conversions as cn
import qnm 
import numpy as np
import matplotlib.pyplot as plt

#qnm.download_data()

#parameters
final_mass=70
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

#220 scalar
grav_220_s = qnm.modes_cache(s=0,l=2,m=2,n=0) #set 0 overtone for the scalar
omega220_s, A, C = grav_220_s(a=final_spin)
f220_s=f_to_Phys(np.real(omega220_s),final_mass)/(2*np.pi)
tau220_s=-1/f_to_Phys(np.imag(omega220_s),final_mass)
delta_f221=f220_s/f221-1
delta_tau221=tau220_s/tau221-1


print("f220: {0:.5f}Hz".format(f220_s))
print("tau220: {0:.5f}s".format(tau220_s))
print("delta_f221: {0:.8f}".format(delta_f221))
print("delta_tau221: {0:.8f}".format(delta_tau221))
print("\n")

#------------------VECTOR FIELD----------------#

print("\ns=1 (Vector field):\n")

#220 scalar
grav_220_v = qnm.modes_cache(s=1,l=2,m=2,n=0) #set 0 overtone for the scalar
omega220_v, A, C = grav_220_v(a=final_spin)
f220_v=f_to_Phys(np.real(omega220_v),final_mass)/(2*np.pi)
tau220_v=-1/f_to_Phys(np.imag(omega220_v),final_mass)
delta_f221=f220_v/f221-1
delta_tau221=tau220_v/tau221-1


print("f220: {0:.5f}Hz".format(f220_v))
print("tau220: {0:.5f}s".format(tau220_v))
print("delta_f221: {0:.8f}".format(delta_f221))
print("delta_tau221: {0:.8f}".format(delta_tau221))
print("\n")


#-----------------SPIN SEQUENCE--------------------#

f = open("sequence_GW.txt", "w")

#GW mode
grav_221 = qnm.modes_cache(s=-2,l=2,m=2,n=1)

for i in range(0,1000,1):
    a_i = i/1000
    omega, A, C = grav_221(a=a_i)
    re_om=np.real(omega)
    im_om=np.imag(omega)
    f.write(str(a_i) + '\t' + str(re_om) + '\t' + str(im_om) + '\n')
    
f = open("sequence_scalar_n=0.txt", "w")

#scalar mode
grav_220_s = qnm.modes_cache(s=0,l=2,m=2,n=0)

for i in range(0,1000,1):
    a_i = i/1000
    omega, A, C = grav_220_s(a=a_i)
    re_om=np.real(omega)
    im_om=np.imag(omega)
    f.write(str(a_i) + '\t' + str(re_om) + '\t' + str(im_om) + '\n') 
f.close()
    
f = open("sequence_scalar_n=1.txt", "w")

#scalar mode
grav_221_s = qnm.modes_cache(s=0,l=2,m=2,n=1)

for i in range(0,1000,1):
    a_i = i/1000
    omega, A, C = grav_221_s(a=a_i)
    re_om=np.real(omega)
    im_om=np.imag(omega)
    f.write(str(a_i) + '\t' + str(re_om) + '\t' + str(im_om) + '\n')    
f.close() 

"""    
f = open("sequence_vector.txt", "w")

#scalar mode
grav_220_v = qnm.modes_cache(s=1,l=2,m=2,n=0)

for i in range(0,1000,1):
    a_i = i/1000
    omega, A, C = grav_220_v(a=a_i)
    re_om=np.real(omega)
    im_om=np.imag(omega)
    f.write(str(a_i) + '\t' + str(re_om) + '\t' + str(im_om) + '\n')
"""   

#--------------------PLOTS----------------------#

a_0, re_om_0, im_om_0 = np.loadtxt("sequence_scalar_n=0.txt", usecols=(0,1,2), unpack=True)
a_1, re_om_1, im_om_1 = np.loadtxt("sequence_scalar_n=1.txt", usecols=(0,1,2), unpack=True)

a_o, re_om_o, im_om_o = np.loadtxt("sequence_scalar_old.txt", usecols=(0,1,2), unpack=True)
a_n, re_om_n, im_om_n = np.loadtxt("sequence_scalar.txt", usecols=(0,1,2), unpack=True)

plt.figure(figsize=(14, 6))

#re om
plt.subplot(121)
plt.plot(a_0, re_om_0, label="n=0")
plt.plot(a_1, re_om_1, label="n=1")
#plt.scatter(a_o, re_om_o, label="Old", color="green")
#plt.scatter(a_n, re_om_n, label="New", color="red")
plt.xlabel('$a_f$')
plt.ylabel('$Re(\omega)$')
plt.legend()

#im om
plt.subplot(122)
plt.plot(a_0, im_om_0, label="n=0")
plt.plot(a_1, im_om_1, label="n=1")
#plt.scatter(a_o, im_om_o, label="Old", color="green")
#plt.scatter(a_n, im_om_n, label="New", color="red")
plt.xlabel('$a_f$')
plt.ylabel('$Im(\omega)$')
plt.legend()

plt.savefig("Geometric_omega_scalar.png")
