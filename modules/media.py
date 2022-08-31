import matplotlib.pyplot as plt
import imageio
import numpy
import scipy as sp
from scipy import signal

def histogram(image):
    img = plt.imread(image)
    plt.hist(img.ravel(), bins=256, range=(0.0, 1.0), fc='k', ec='k')

def SPL(p, p0 = 20 * (10**(-6))):
    return 20 * numpy.log( p / p0 )

def MPEG1_II_subpasm_ammount():
    return 32

def quantization(image):
    lena = imageio.imread(image)
    #quantization
    lena_quant_simple = quantizer_simple  (lena, qstep=16)
    lena_quant_dead   = quantizer_deadzone(lena, qstep=16, deadzone=3.0)
    #display images
    figImg, axsImg = plt.subplots(1, 3, figsize=[24, 8])
    axsImg[0].imshow(lena,              cmap=plt.cm.gray, vmin=0, vmax=255)
    axsImg[1].imshow(lena_quant_simple, cmap=plt.cm.gray, vmin=0, vmax=255)
    axsImg[2].imshow(lena_quant_dead  , cmap=plt.cm.gray, vmin=0, vmax=255)
    #display histograms
    figH, axsH = plt.subplots(1, 3, figsize=[24, 8])
    axsH[0].hist(lena.ravel().astype(int), bins=256, range=[0, 256])
    axsH[0].set_title("Default")
    axsH[1].hist(lena_quant_simple.ravel().astype(int), bins=256, range=[0, 256])
    axsH[1].set_title("Quant_simple")
    axsH[2].hist(lena_quant_dead.ravel().astype(int), bins=256, range=[0, 256])
    axsH[2].set_title("Quant_dead")

def RGB(image):
    #print images
    im = imageio.imread(image)
    R = im[:, :, 0]
    G = im[:, :, 1]
    B = im[:, :, 2]
    z = np.zeros_like(R)
    plt.subplot(2, 3, 1)
    plt.imshow(R, cmap=plt.cm.gray)
    plt.subplot(2, 3, 2)
    plt.imshow(G, cmap=plt.cm.gray)
    plt.subplot(2, 3, 3)
    plt.imshow(B, cmap=plt.cm.gray)
    plt.subplot(2, 3, 4)
    plt.hist(R.ravel(), range(0, 255))
    plt.subplot(2, 3, 5)
    plt.hist(G.ravel(), range(0, 255))
    plt.subplot(2, 3, 6)
    plt.hist(B.ravel(), range(0, 255))

def RGBtoYCbCr(RGB):
    R = RGB[:, :, 0]
    G = RGB[:, :, 1]
    B = RGB[:, :, 2]
    Y = 0.21260*R + 0.71520*G + 0.07220*B
    Cb = -0.11457*R - 0.38543*G + 0.50000*B
    Cr = 0.50000*R - 0.45415*G - 0.04585*B
    ImageYCbCr = np.stack((Y, Cb, Cr), axis=2)
    return ImageYCbCr

def addConstant(image,constant):
    im = copy.copy(image)
    im.astype(np.int16)
    im += constant
    np.clip(im, 0, 255)
    im.astype(np.uint8)
    return im

def binarizeImage(image,treshold):
    im = copy.copy(image)
    im.astype(np.int16)
    im = np.where( im < treshold, 0, 255 )
    np.clip(im, 0, 255)
    im.astype(np.uint8)
    return im

def image_histogram_normalization(image):
    im = copy.copy(image)
    im.astype(np.int16)
    max = np.max(im)
    min = np.min(im)
    im = (im - min) / (max - min) * (255)
    np.clip(im, 0, 255)
    im.astype(np.uint8)
    return im

def image_histogram_equalization(a):
    a = np.array(a)
    bins = np.linspace(0.0, 255, 257)
    hist, bins2 = np.histogram(a, bins=bins)

    cdf = np.cumsum(hist, dtype=np.float64)
    cdf = np.hstack(([0], cdf))
    cdf = cdf / cdf[-1]
    
    binnum = np.digitize(a, bins, True)-1
    neg = np.where(binnum < 0)
    binnum[neg] = 0
    
    aeq = cdf[binnum] * bins[-1]
    
    return aeq

def apply_gamma(image, gamma=1.0):
    im = copy.copy(image)
    im.astype(np.int16)
    im = (im/255)**(1/gamma) * 255
    np.clip(im, 0, 255)
    im.astype(np.uint8)
    return im

def calculateSpectrums(Image) : 
    f = np.fft.fft2(Image)
    magnitude_boats = np.abs(f)
    magnitude_log_boats = np.log(magnitude_boats)
    phase_boats = np.angle(f)   
    return magnitude_boats, magnitude_log_boats, phase_boats

def reconstruction_from_spectrum(magnitude_spectrum, phase_spectrum):
    rec = magnitude_spectrum * np.e ** ( 1j * phase_spectrum)
    rec = np.fft.ifft2(rec)
    rec_image = np.clip(rec.astype(np.uint8), 0, 255)
    return rec_image

def HPFilter(image):
    Mask = [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]
    image = sp.signal.convolve2d(image, Mask, boundary='wrap', mode='same')
    return image

def BorderDetectFilter(image):
    Mask = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    image = sp.signal.convolve2d(image, Mask, boundary='wrap', mode='same')
    return image
