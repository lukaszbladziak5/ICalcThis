import numpy

def numericAperture(n0, n1, n2):
#       _______________________
#       |
#    \  |______________________
#     \ | n1    /\        /\
#      \|      /  \      /  \
#       |\----/----\----/----\ ...
#       | \  /      \  /
#  n0   |  \/        \/
#       |______________________
#       | n2
#       |______________________
#
    return (1 / n0) * numpy.sqrt(n1**2 - n2**2)

def opticalBandwidth(NA, n, L):
    #Przykład:
    #n1=1,49; NA=0,297; dla L=1km
    #tm = 98,67ns B3dB(opt) x L= 4,47MHz*km
    return NA**2 / (2 * 3 * 10**5 * n) * L

def modLatency(a, Lambda, NA):
    return ((2* numpy.pi * a) / Lambda) * NA

def insertionLoss(P0, P1):
    return -10 * numpy.log(P0 / P1)

def reflectionnLoss(Pr, Pi):
    return -10 * numpy.log(Pr / Pi)

def diameterLoss(D1, D2):
    #----------------------|    |-------------------------
    #                      |    |-------------------------
    #----------------------|    |           |
    #       | D1           |    |           |  D2
    #----------------------|    |           |
    #                      |    |-------------------------
    #----------------------|    |-------------------------
    if(D2 >= D1): return 0
    return -10 * numpy.log( (D1/D2)**2 )

def NALoss(NA1, NA2):
    #----------------------|  / _     |-------------------------
    #                      | /   \_   |
    #                      |/      \_ |
    #                      |\ NA1 NA2\|
    #                      | \      _/|
    #                      |  \   _/  |
    #----------------------|   \ /    |-------------------------
    if(NA2 >= NA1): return 0
    return 10 * numpy.log( (NA1/NA2)**2 )

def profileLoss(g1, g2):
    if(g1 > g2): return 0
    return 10 * numpy.log( (g1*(g2+2)) / (g2*(g1+2)) )

def axisShift(R, x, a):
    #----------------------| /---|-------------------------
    #              /\      |/ a  |-------------------------
    #--------------||------|-----|           
    #              ||  R   |     |           
    #--------------\/------|  x  |           
    #                      |-----|-------------------------
    #----------------------|     |-------------------------
    return -20 * numpy.log( (R + x * numpy.tan(a)) / R)

def radialShift(R, y):
    #----------------------|      /\
    #                      |      || y
    #----------------------|    |-\/-----------------           
    #                      |    |
    #----------------------|    |--------------------
    #                      |    |
    #----------------------|    |
    #SM ONLY
    return - 10 * numpy.log( 1/numpy.pi* ( 2*numpy.arccos(y / (2*R)) - (y/R) * (1 - (y/(2*R)**2)) )**(1/2) )

def fresnelReflection(R):
    return - 10 * numpy.log(1 - R)

