'''
This script governs all the mathmematics which are used in the measurement
'''

###################################################################
######################  Function definitions  #####################
###################################################################

# Any necessary library imports
import cmath
import numpy as np
from math import *

def arcotan(im,re):
    tan=0
    if im>=0.0 and re>=0.0:
        if re==0:
            re=10**-20
        tan=atan(im/re)
    if im>=0.0 and re<=0.0:
        if im==0:
            im=10**-20
        tan=pi/2+atan(abs(re)/im)
    if im<=0.0 and re<=0.0:
        if re==0:
            re=10**-20
        tan=pi+atan(abs(im)/abs(re))
    if im<=0.0 and re>=0.0:
        if im==0:
            im=10**-20
        tan=(3*pi/2)+atan(re/abs(im))
    return tan

def trunca(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    slen = len('%.*f' % (n, f))
    return str(f)[:slen]


# This function computes the matrix M = <VV*>
def compute_m_T(V, Vconj):
    M = np.mat((4,4))
    M = np.dot(np.mat(V).T,np.mat(Vconj))
    return M

def compute_M(V, Vconj):
    M = np.mat((4,4))
    M = np.dot(np.mat(V).H,np.mat(Vconj))
    return M

# This function computes the magnitude coefficients of the gain matrix G
def compute_mag(V):
    magnitude = np.zeros(4)
    for i in range(len(V)):
        magnitude[i] = ((V.real[i])**2+(V.imag[i])**2)**0.5
    return magnitude


# Compute the relative phases of the gain matrix G
def compute_relative_phase(V):
    rel_phase = np.zeros(4)
    for i in range(0,4):
		rel_phase[i]=arcotan(V.real[i],V.imag[i])*180/(np.pi) #en grados
    return rel_phase

def c_angle(re,im):#complex angle / evaluates atan(Im/Re) for the 4 cuadrants
# initializing
    out=0
    if re==0:
        re=10**-20
    if im==0:
        im=10**-20
# Angle calculation
    if im>=0.0 and re>=0.0:
        out=atan(im/re)
    if im>=0.0 and re<=0.0:
        out=pi/2+atan(abs(re)/im)
    if im<=0.0 and re<=0.0:
        out=pi+atan(abs(im)/abs(re))
    if im<=0.0 and re>=0.0:
        out=(3*pi/2)+atan(re/abs(im))
    return out # the output is in radians

def compute_mag_ratio(magnitude,probe):
    if magnitude[probe]==0 or magnitude[probe+1]==0 :
        amp_ratio=0.555555555555555555555555
    else:
        amp_ratio = magnitude[probe]/magnitude[probe+1]
        print('The Amplitude Ratio is: '+ str(amp_ratio))
    return amp_ratio

def compute_phase_diff(rel_phase,probe):
    phase_diff = rel_phase[probe]-rel_phase[probe+1]
    print('The Phase difference is: ' + str(phase_diff))
    return phase_diff

# Compute the power of the spectral channels
def channel_power(spectrum_z1_a, spectrum_z1_c, spectrum_z0_a, spectrum_z0_c):
    power_spectrum_z1_a = 10*np.log10(abs(spectrum_z1_a)**2)
    power_spectrum_z1_c = 10*np.log10(abs(spectrum_z1_c)**2)
    power_spectrum_z0_a = 10*np.log10(abs(spectrum_z0_a)**2)
    power_spectrum_z0_c = 10*np.log10(abs(spectrum_z0_c)**2)
    index1 = np.argmax(power_spectrum_z1_a, axis = 0)
    index2 = np.argmax(power_spectrum_z1_c, axis = 0)
    index3 = np.argmax(power_spectrum_z0_a, axis = 0)
    index4 = np.argmax(power_spectrum_z0_c, axis = 0)
    print("The maximum of the spectrum are at channel: "+ str(index1) + ', ' + str(index2) + ', ' + str(index3) + ', ' + str(index4))
    return power_spectrum_z1_a, power_spectrum_z1_c, power_spectrum_z0_a, power_spectrum_z0_c

# Do a sanity check on the data. If all goes well this should check out and all should return 0 or close too 0.
def consistency_magnitude(M):
    consistent = np.zeros((4,4))
    for i in range(4):
        for j in range(4):
            consistent[i][j] = abs(M[i,j])**2-abs(M[i,i])*abs(M[j,j])
    print 'Consistency magnitude check (should be zero or close to 0)'
    print consistent  

# A second sanity check on the data. The resulting matrix should be zero or a multiple of 2pi.
def consistency_phase(M):
    # First number in each row is M_{i,k} and the following numbers are M_{i,j}+M_{j,k}
    consistent_phase = np.zeros((4,4))
    for i in range(4):
        consistent_phase[i,0] = cmath.phase(M[i,i])
    consistent_phase[0,1] = (cmath.phase(M[0,1])+cmath.phase(M[1,0]))
    consistent_phase[0,2] = (cmath.phase(M[0,2])+cmath.phase(M[2,0]))
    consistent_phase[0,3] = (cmath.phase(M[0,3])+cmath.phase(M[3,0]))
    consistent_phase[1,1] = (cmath.phase(M[1,0])+cmath.phase(M[0,1]))
    consistent_phase[1,2] = (cmath.phase(M[1,2])+cmath.phase(M[2,1]))
    consistent_phase[1,3] = (cmath.phase(M[1,3])+cmath.phase(M[3,1]))
    consistent_phase[2,1] = (cmath.phase(M[2,0])+cmath.phase(M[0,2]))
    consistent_phase[2,2] = (cmath.phase(M[2,1])+cmath.phase(M[1,2]))
    consistent_phase[2,3] = (cmath.phase(M[2,3])+cmath.phase(M[3,2]))
    consistent_phase[3,1] = (cmath.phase(M[3,0])+cmath.phase(M[0,3]))
    consistent_phase[3,2] = (cmath.phase(M[3,1])+cmath.phase(M[1,3]))
    consistent_phase[3,3] = (cmath.phase(M[3,2])+cmath.phase(M[2,3]))
    print '\nConsistency phase check (should be zero or a multiple of 2pi)'
    print consistent_phase
    return consistent_phase

# A function to find the index of the position of the maximum in a matrix
def find_maximum(magnitude):
    index = np.argmax(magnitude, axis = 0)
    return index

# Since we only concern ourselves with one channel at a time we extract only the vectors V and V* from the whole array which is read from the ROACH
def voltage(real_spectrum1, real_spectrum1conj, imag_spectrum1, imag_spectrum1conj, real_spectrum2, real_spectrum2conj, imag_spectrum2, imag_spectrum2conj, real_spectrum3, real_spectrum3conj, imag_spectrum3, imag_spectrum3conj, real_spectrum4, real_spectrum4conj, imag_spectrum4, imag_spectrum4conj, channel_number):
    V = np.array([ real_spectrum1[channel_number]+1j*imag_spectrum1[channel_number], real_spectrum2[channel_number]+1j*imag_spectrum2[channel_number], real_spectrum3[channel_number]+1j*imag_spectrum3[channel_number], real_spectrum4[channel_number]+1j*imag_spectrum4[channel_number] ])
    Vconj = np.array([ real_spectrum1[channel_number]+1j*imag_spectrum1conj[channel_number], real_spectrum2conj[channel_number]+1j*imag_spectrum2conj[channel_number], real_spectrum3conj[channel_number]+1j*imag_spectrum3conj[channel_number], real_spectrum4conj[channel_number]+1j*imag_spectrum4conj[channel_number] ])
    return V,Vconj

def generate_matrix_list(rows, columns):
    matrix = []

    for cont0 in range(rows):
        row = []
        for cont1 in range(columns):
            row.append(0)
        matrix.append(row)

    return matrix

#
# if __name__ == '__main__':
#     lol = generate_matrix_list(2,8)
#
#     lol[0][5] = 2
#     lol[1][1] = 2
#
#     print lol
