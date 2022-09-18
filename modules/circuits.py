import numpy as np

#Basic components equivalents
def resistorSeries(R1, R2):
    #
    # --[R1]--[R2]--
    #
    return R1 + R2

def resistorParallel(R1, R2):
    #--|-------|
    # [  ]    [  ]
    # [R1]    [R2]
    # [  ]    [  ]
    #--|-------|
    try:
        return (R1 * R2) / (R1 + R2)
    except:
        return ("NaN")

def capacitorSeries(C1, C2):
    #
    # --[C1]--[C2]--
    #
    try:
        return (C1 * C2) / (C1 + C2)
    except:
        return ("NaN")

def capacitorParallel(C1, C2):
    #--|-------|
    # [  ]    [  ]
    # [C1]    [C2]
    # [  ]    [  ]
    #--|-------|
    return C1 + C2

#Ohma's law
#R = U / I
#Appliable for impedance (R replaced by Z)
def ohmLawR(U, I):
    return U / I

def ohmLawU(R, I):
    return R * I

def ohmLawI(R, U):
    return U / R

#Power
def powerUI(U, I):
    return U * I

def powerIR(I, R):
    return (I ** 2) * R

#Root mean square (voltage and current)
def RMS(MAX):
    return MAX / np.sqrt(2)
