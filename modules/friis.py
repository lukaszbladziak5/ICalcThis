import numpy

def exec(Gt, Gr, wavelength, d): #Pr/Pt
    return Gt*Gr * ((wavelength / (4*numpy.pi*d))**2)

def execPr(Gt, Gr, wavelength, d, Pt):
    return Gt*Gr * ((wavelength / (4*numpy.pi*d))**2)*Pt

def execPt(Gt, Gr, wavelength, d, Pr):
    return Pr / (Gt*Gr * ((wavelength / (4*numpy.pi*d))**2))
