import matplotlib.pyplot as plt
from numpy import log

def histogram(image):
    img = plt.imread(image)
    plt.hist(img.ravel(), bins=256, range=(0.0, 1.0), fc='k', ec='k')

def SPL(p, p0 = 20 * (10**(-6))):
    return 20 * numpy.log( p / p0 )

def MPEG1_II_subpasm_ammount():
    return 32

#More to be added (copied from WDM) soon