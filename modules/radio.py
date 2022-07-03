#Friss formula in friss.py

from numpy import sqrt, pi

def waveToFreq(waveLength):
    return 300000 / waveLength #in kHz

def freqToWave(freq):
    return 300000 / freq #in kHz

def eirp(power, loss, gain):
    #P - output power dBm
    #G - antenna gain dBi
    #O - cable and connector losses dB
    return power - loss + gain

def fresnal(distance, freq):
    #distance in km, freq in GHz
    #Returns radius in meters
    return 17.31 * numpy.sqrt(D / (4 * freq))

def dipoleLength(freq):
    #
    #                L
    # |------------------------------|
    #        E
    # |--------------|
    #
    # ===============\/===============
    #                ||
    #
    #Total length (L) of dipole antenna, divide result by 2 for one (E)
    return 468 / freq * 0.3048

def effectiveAperture(waveLength, gain):
    #Result in m^2
    return (waveLength ** 2) / (4 * numpy.pi) * gain

#Plain wave
#e - relative permittivity
#u - relative permeability
def plainWaveVelocity(freq, e, u):
    #Phase velocity in m/s
    return 300000/ numpy.sqrt(u * e)

def plainWaveImpedance(freq, e, u):
    return 377 * numpy.sqrt(u / e)

def powerBudget(PTx, LTx, LRx, LFS, LM = 0, GTx = 0, GRx = 0):
    #LM for misc. losses
    #All in dB
    return PTx + GTx - LTx - LFS - LM+ GRx - LRx

def SAR(E, m, c):
    #E - electric field (RMS) in V/m
    #C - conductivity of material in S/m
    #m - mass density in Kg/m^3
    return (E ** 2 * c ) / m

#TD