import math

def ratioTodB(P1, P2):
    if (P1 <= 0) or (P2 <= 0): raise ValueError("dB calculator: values cannot be equal or lower than 0.0")
    return 10*math.log10(P1/P2) #dB #6
def lossTodB(P):
    if (P > 1) or (P <= 0):
        raise ValueError("dB calculator: loss cannot be bigger than 1.0 and value equal or lower than 0.0 ")
    return 10*math.log(P) #dB #7
def voltageTodB(V1, V2):
    if (V1 <= 0) or (V2 <= 0): raise ValueError("dB calculator: values cannot be equal or lower than 0.0")
    return 20*math.log10(V1/V2) #dB #8
def WTodBm(P):
    if (P <= 0): raise ValueError("dB calculator: value cannot be equal or lower than 0.0")
    return 10*math.log10(P/1) #dBW (can be used for mW and uW - same formula, change unit) #4
def dBWTodBm(dBW): return dBW + 30 #dBm #0
def dBmTodBW(dBm): return dBm - 30 #dBW #1
def dBToRatio(dB): return 10**(dB/10) #Ratio #5
def dBWToW(dBW): return 10**(dBW/10) #W #2
def dBmToW(dBm): return 10**(dBm/10) / 1000 #W #3